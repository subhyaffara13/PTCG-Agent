
def native_layer_norm(
    input: list[int], normalized_shape: list[int]
) -> tuple[list[int], list[int], list[int]]:
    reduction_shape: list[int] = []
    num_unreduced_dimensions = len(input) - len(normalized_shape)
    if num_unreduced_dimensions < 0:
        raise AssertionError(
            f"Expected len(input) ({len(input)}) >= len(normalized_shape) "
            f"({len(normalized_shape)})"
        )
    for i in range(num_unreduced_dimensions):
        reduction_shape.append(input[i])
    for i in range(num_unreduced_dimensions, len(input)):
        reduction_shape.append(1)
    return _copy(input), reduction_shape, reduction_shape


def native_layer_norm(
    input: Tensor,
    normalized_shape: ShapeType,
    weight: Tensor | None,
    bias: Tensor | None,
    eps: float,
) -> tuple[Tensor, Tensor, Tensor]:
    from torch.fx.experimental.symbolic_shapes import sym_eq

    normalized_ndim = len(normalized_shape)
    torch._check(
        normalized_ndim >= 1,
        lambda: "Expected normalized_shape to be at least 1-dimensional, i.e., "
        + "containing at least one element, but got normalized_shape = "
        + str(normalized_shape),
    )
    # torch.Size([1, 2, 3]) == [1, 2, 3] evaluates to False
    # while torch.Size([1, 2, 3]) == (1, 2, 3) is True
    # therefore we use tuple(normalized_shape)
    torch._check(
        # pyrefly: ignore [bad-argument-type]
        weight is None or sym_eq(weight.shape, tuple(normalized_shape)),
        lambda: "Expected weight to be of same shape as normalized_shape, but got "
        + "weight of shape "
        + str(weight.shape)  # type: ignore[union-attr]
        + " and normalized_shape = "
        + str(normalized_shape),
    )
    torch._check(
        # pyrefly: ignore [bad-argument-type]
        bias is None or sym_eq(bias.shape, tuple(normalized_shape)),
        lambda: "Expected bias to be of same shape as normalized_shape, but got "
        + "bias of shape "
        + str(bias.shape)  # type: ignore[union-attr]
        + " and normalized_shape = "
        + str(normalized_shape),
    )
    torch._check(
        input.ndim >= normalized_ndim
        and sym_eq(
            input.shape[(input.ndim - normalized_ndim) :],
            tuple(normalized_shape),
        ),
        lambda: "Given normalized_shape="
        + str(normalized_shape)
        + ", expected input with shape "
        + str(normalized_shape)
        + ", but got input of size "
        + str(input.shape),
    )
    torch._check(
        not input.is_complex(),
        lambda: "native_layer_norm does not support complex inputs",
    )

    input = contiguous(input)
    if weight is not None:
        weight = contiguous(weight)
    if bias is not None:
        bias = contiguous(bias)

    axis = input.ndim - normalized_ndim
    reduction_dims = list(range(axis, input.ndim))
    out, mean, rstd = _normalize(input, reduction_dims, eps)

    if weight is None and bias is not None:
        out = out + bias
    elif weight is not None and bias is None:
        out = out * weight
    elif weight is not None and bias is not None:
        out = out * weight + bias

    out = _maybe_convert_to_dtype(out, input.dtype)  # type: ignore[assignment]
    if input.device.type in ["cpu", "mtia"]:
        mean = _maybe_convert_to_dtype(mean, input.dtype)  # type: ignore[assignment]
        rstd = _maybe_convert_to_dtype(rstd, input.dtype)  # type: ignore[assignment]
    return (out, mean, rstd)


def native_layer_norm(
    g: jit_utils.GraphContext,
    input: _C.Value,
    normalized_shape: Sequence[int],
    weight: _C.Value,
    bias: _C.Value,
    eps: float,
) -> tuple[_C.Value, _C.Value, _C.Value]:
    axes = [-i for i in range(len(normalized_shape), 0, -1)]

    two_cst = symbolic_helper._generate_wrapped_number(g, 2.0)
    eps_cst = symbolic_helper._generate_wrapped_number(g, eps)

    if g.opset < 18:
        mean = g.op("ReduceMean", input, axes_i=axes)
    else:
        mean = g.op(
            "ReduceMean",
            input,
            g.op("Constant", value_t=torch.tensor(axes, dtype=torch.long)),
        )

    numerator = sub(g, input, mean)

    # Cast it to eps dtype to avoid precision loss
    is_type_half = (
        _type_utils.JitScalarType.from_value(numerator)
        == _type_utils.JitScalarType.HALF
    )
    if is_type_half:
        eps_dtype = _type_utils.JitScalarType.from_value(eps_cst)
        numerator = g.op(
            "Cast", numerator, to_i=_type_utils.JitScalarType(eps_dtype).onnx_type()
        )

    # variance = e((x - e(x))^2), and (x - e(x)) is the numerator in the layer_norm formula
    if g.opset < 18:
        # pyrefly: ignore [no-matching-overload]
        variance = g.op("ReduceMean", pow(g, numerator, two_cst), axes_i=axes)
    else:
        variance = g.op(
            "ReduceMean",
            # pyrefly: ignore [no-matching-overload]
            pow(g, numerator, two_cst),
            g.op("Constant", value_t=torch.tensor(axes, dtype=torch.long)),
        )

    denominator = sqrt(g, g.op("Add", variance, eps_cst))
    normalized = g.op("Div", numerator, denominator)

    # Cast back to input type as eps related ops are all done
    if is_type_half:
        input_dtype = _type_utils.JitScalarType.from_value(input)
        normalized = g.op(
            "Cast", normalized, to_i=_type_utils.JitScalarType(input_dtype).onnx_type()
        )

    if not (weight is None or symbolic_helper._is_none(weight)):
        normalized = mul(g, normalized, weight)
    if not (bias is None or symbolic_helper._is_none(bias)):
        normalized = add(g, normalized, bias)

    # rdenominator := 1 / sqrt(variance + eps)
    # According to aten::native_layer_norm, rdenominator should have the same dtype as input,
    # mean and normalized, so we need to Cast it back
    if is_type_half:
        denominator = g.op(
            "Cast",
            denominator,
            to_i=_type_utils.JitScalarType(input_dtype).onnx_type(),  # type: ignore[possibly-undefined]
        )
        rdenominator = g.op("Reciprocal", denominator)
    else:
        rdenominator = reciprocal(g, denominator)

    return normalized, mean, rdenominator

