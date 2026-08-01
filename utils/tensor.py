
def tensor(data, *, dtype=None, device=None, layout=None, pin_memory=False):
    assert_nyi(layout in (None, torch.strided), f"layout={layout}")
    assert_nyi(not pin_memory, "pin_memory")
    if isinstance(_unwrap(data), int):
        dtype = dtype or torch.int64
    else:
        dtype = dtype or torch.get_default_dtype()

    ranges: list[sympy.Expr] = []

    if isinstance(data, sympy.Basic):

        def inner_fn(index):
            return ops.index_expr(data, dtype)

    elif isinstance(data, (float, int)):

        def inner_fn(index):
            return ops.constant(data, dtype)

    elif len(data) == 0 or isinstance(data[0], (float, int)) and len(data) <= 8:
        # inline small tensors
        ranges.append(sympy.Integer(len(data)))

        def inner_fn(index):
            def binary_search(start, end):
                assert start < end
                if end - start == 1:
                    return ops.constant(data[start], dtype)
                mid = (end - start) // 2 + start
                return ops.where(
                    ops.lt(
                        ops.index_expr(index[0], torch.int64),
                        ops.constant(mid, torch.int64),
                    ),
                    binary_search(start, mid),
                    binary_search(mid, end),
                )

            if len(data) == 0:
                return ops.constant(0, dtype)
            return binary_search(0, len(data))

    else:
        return V.graph.add_tensor_constant(
            torch.tensor(data, dtype=dtype, device=device)
        )

    return Pointwise.create(
        device=decode_device(device),
        dtype=dtype,
        inner_fn=inner_fn,
        ranges=ranges,
    )


def tensor(data, *, dtype=None, device=None, pin_memory=False, requires_grad=False):
    # TODO (or not): support names kwarg
    if isinstance(data, torch.Tensor):
        warnings.warn(
            "To copy construct from a tensor, it is recommended to use sourceTensor.detach().clone() "
            "or sourceTensor.detach().clone().requires_grad_(True), rather than torch.tensor(sourceTensor)",
            UserWarning,
            stacklevel=2,
        )
    type_inference = dtype is None
    new_tensor = _internal_new_from_data(
        # device="cpu" because that's what you get with torch.tensor(2) no
        # device by default
        {"device": "cpu"},  # TODO: use torch.get_default_tensor_type
        dtype if dtype is not None else torch.get_default_dtype(),
        device,
        data,
        copy_variables=True,
        copy_numpy=True,
        type_inference=type_inference,
        pin_memory=pin_memory,
    )
    new_tensor.detach_()
    if requires_grad:
        new_tensor.requires_grad_(requires_grad)
    return new_tensor


def tensor(draw, shapes=None, elements=None, qparams=None, dtype=np.float32):
    if isinstance(shapes, SearchStrategy):
        _shape = draw(shapes)
    else:
        _shape = draw(st.sampled_from(shapes))
    if qparams is None:
        if elements is None:
            elements = floats(-1e6, 1e6, allow_nan=False, width=32)
        X = draw(stnp.arrays(dtype=dtype, elements=elements, shape=_shape))
        assume(not (np.isnan(X).any() or np.isinf(X).any()))
        return X, None
    qparams = draw(qparams)
    if elements is None:
        min_value, max_value = _get_valid_min_max(qparams)
        elements = floats(min_value, max_value, allow_infinity=False,
                          allow_nan=False, width=32)
    X = draw(stnp.arrays(dtype=dtype, elements=elements, shape=_shape))
    # Recompute the scale and zero_points according to the X statistics.
    scale, zp = _calculate_dynamic_qparams(X, qparams[2])
    enforced_zp = _ENFORCED_ZERO_POINT.get(qparams[2], None)
    if enforced_zp is not None:
        zp = enforced_zp
    return X, (scale, zp, qparams[2])


def tensor(
    g: jit_utils.GraphContext, data, dtype=None, device=None, requires_grad=False
):
    dtype = symbolic_helper._get_const(dtype, "i", "dtype")
    if symbolic_helper._is_packed_list(data):
        if dtype is None:
            dtype = _type_utils.JitScalarType.from_value(
                symbolic_helper._unpack_list(data)[0]
            )
        input_list = []
        for t in symbolic_helper._unpack_list(data):
            shape_reference = g.op("Constant", value_t=torch.LongTensor([1]))
            t = symbolic_helper._reshape_helper(g, t, shape_reference)
            t = g.op("Cast", t, to_i=_type_utils.JitScalarType(dtype).onnx_type())
            input_list.append(t)
        return g.op("Concat", *input_list, axis_i=0)
    else:
        if dtype is None:
            dtype = _type_utils.JitScalarType.from_value(data)
        if symbolic_helper._is_list(data) and (
            symbolic_helper._is_tensor_list(data)
            or symbolic_helper._is_scalar_list(data)
        ):
            data = g.op("ConcatFromSequence", data, axis_i=0, new_axis_i=1)
    return g.op("Cast", data, to_i=_type_utils.JitScalarType(dtype).onnx_type())


def tensor(*shape, element_type: Type = None, encoding: Optional[str] = None):
    if encoding is not None:
        encoding = StringAttr.get(encoding)
    if not shape or (len(shape) == 1 and isinstance(shape[-1], Type)):
        if encoding is not None:
            raise ValueError("UnrankedTensorType does not support encoding.")
        return _shaped(
            *shape, element_type=element_type, type_constructor=UnrankedTensorType.get
        )
    return _shaped(
        *shape,
        element_type=element_type,
        type_constructor=partial(RankedTensorType.get, encoding=encoding),
    )

