
def convolution(
    x: TensorBox,
    weight: TensorBox,
    bias: TensorBox | None,
    stride: Sequence[int],
    padding: Sequence[int],
    dilation: Sequence[int],
    transposed: bool,
    output_padding: Sequence[int],
    groups: int,
):
    stride = tuple(stride)
    padding = tuple(padding)
    dilation = tuple(dilation)
    output_padding = tuple(output_padding)
    if not isinstance(groups, int):
        groups = V.graph.sizevars.guard_int(groups)
    assert isinstance(groups, int)

    # Need use hint for triton template since the template does not
    # work with a dynamic shape.
    #
    # No need to guard_int for dilation and output_padding
    # since the template is only used when dilation is 1 and output_padding
    # is 0.
    stride = tuple(V.graph.sizevars.guard_int_seq(stride))
    padding = tuple(V.graph.sizevars.guard_int_seq(padding))

    kwargs: ConvLayoutParams = {
        "stride": stride,
        "padding": padding,
        "dilation": dilation,
        "transposed": transposed,
        "output_padding": output_padding,
        "groups": groups,
    }

    device_type = ir.get_device_type(x)

    if len(x.get_size()) == len(weight.get_size()) - 1:
        # add batch dimension to simplify rest of function
        return L[aten.squeeze](
            convolution(L[aten.expand](x, [1, *x.get_size()]), weight, bias, **kwargs),
            dim=0,
        )

    out_chan, in_chan, *kernel_shape = V.graph.sizevars.guard_int_seq(weight.get_size())

    # Always convert conv1D to 2D for Intel GPU.
    # Only conv2D can be converted to channel last layout,
    # which have much better performance.
    if len(x.get_size()) == 3 and len(kernel_shape) == 1 and device_type == "xpu":
        kwargs.update(
            {
                "stride": (1,) + stride,
                "padding": (0,) + padding,
                "dilation": (1,) + dilation,
                "output_padding": (0,) + output_padding,
            }
        )
        # (N, C, L) -> (N, C, 1, L)
        x = L[aten.unsqueeze](x, dim=2)
        weight = L[aten.unsqueeze](weight, dim=2)

        return L[aten.squeeze](
            convolution(x, weight, bias, **kwargs),
            dim=2,
        )

    ndim = len(kernel_shape)
    stride = pad_listlike(stride, ndim)
    padding = pad_listlike(padding, ndim)
    dilation = pad_listlike(dilation, ndim)
    output_padding = pad_listlike(output_padding, ndim)

    def channels_last_conv():
        if V.graph.layout_opt and ndim == 2:
            return True

        layout = conv_layout(x, weight, None, **kwargs)
        # TODO: This does not guard on the stride order decision,
        # shall we use optimization_hint to handle unbacked?
        req_stride_order = ir.get_stride_order(
            V.graph.sizevars.guarding_hints_or_throw(layout.stride)
        )
        return req_stride_order == ir.NHWC_STRIDE_ORDER

    autotuning_gemm = config.max_autotune or config.max_autotune_gemm

    if (
        (config.conv_1x1_as_mm or (autotuning_gemm and channels_last_conv()))
        and is_ones(kernel_shape)
        and is_ones(stride)
        and is_zeros(padding)
        and is_ones(dilation)
        and not transposed
        and is_zeros(output_padding)
        and groups == 1
        and V.graph.sizevars.statically_known_gt(sympy_product(x.get_size()), 0)
    ):
        return convert_1x1_conv_to_mm(x, weight, bias)

    if bias is not None and device_type != "cpu":
        # peel off the bias, cudnn is slower with it
        result = convolution(x, weight, None, **kwargs)
        return L[aten.add](
            result, L[aten.view](bias, [result.get_size()[1]] + ndim * [1])
        )

    x.realize()
    weight.realize()

    # ndim can be 1 for convolution in models such as demucs
    # TODO: check if it's beneficial to convert Conv1d to Conv2d and then
    # apply channels last.
    if V.graph.layout_opt and ndim == 2:
        V.graph.num_channels_last_conv += 1
        x = ir.ExternKernel.require_channels_last(x)  # type: ignore[assignment]
        # TODO maybe we can convert weights to channels last just once before
        # running the model.
        weight = ir.ExternKernel.require_channels_last(weight)  # type: ignore[assignment]
        layout = conv_layout(x, weight, None, **kwargs)
    else:
        layout = conv_layout(x, weight, None, **kwargs)
        # TODO: This does not guard on the stride order decision,
        # shall we use optimization_hint to handle unbacked?
        req_stride_order = ir.get_stride_order(
            V.graph.sizevars.guarding_hints_or_throw(layout.stride)
        )
        x = ir.ExternKernel.require_stride_order(x, req_stride_order)  # type: ignore[assignment]
        weight = ir.ExternKernel.require_stride_order(weight, req_stride_order)  # type: ignore[assignment]

    ordered_kwargs_for_cpp_kernel = [
        "stride",
        "padding",
        "dilation",
        "transposed",
        "output_padding",
        "groups",
    ]
    if bias is None:
        args = [x, weight]
        kwargs["bias"] = None  # type: ignore[typeddict-unknown-key]
        ordered_kwargs_for_cpp_kernel.insert(0, "bias")
    else:
        args = [x, weight, bias]
        bias.realize()
        bias.freeze_layout()
        V.graph.sizevars.guard_int_seq(bias.get_size())

    choices = []
    if torch._inductor.utils._use_conv_autotune_backend("ATEN"):
        choices = [
            aten_convolution.bind(
                args,
                layout,
                ordered_kwargs_for_cpp_kernel,
                **kwargs,
            )
        ]

    if (
        torch._inductor.utils._use_conv_autotune_backend("TRITON")
        and use_triton_template(layout)
        # templates only support these:
        and is_ones(dilation)
        and not transposed
        and is_zeros(output_padding)
        # there are some odd models where this check fails (e.g. shufflenet_v2_x1_0)
        and V.graph.sizevars.statically_known_equals(in_chan * groups, x.get_size()[1])  # type: ignore[arg-type]
    ):
        if (
            is_ones(kernel_shape)
            and is_ones(stride)
            and is_zeros(padding)
            and groups == 1
        ):
            choices.append(aten_conv1x1_via_mm.bind(args, layout))

        is_depthwise = groups > 1 and in_chan == 1 and out_chan == groups
        if is_depthwise and ndim == 1:
            depthwise_configs = V.choices.get_depthwise_conv_configs(device_type)
            for cfg in depthwise_configs:
                depthwise_conv1d_template.maybe_append_choice(
                    choices,
                    input_nodes=(x, weight),
                    layout=layout,
                    KERNEL_SIZE=kernel_shape[0],
                    CONV_STRIDE=stride[0],
                    PADDING=padding[0],
                    num_stages=cfg.num_stages,
                    num_warps=cfg.num_warps,
                    **cfg.kwargs,
                )

        conv_configs = V.choices.get_conv_configs(device_type)

        dtype_size = x.get_dtype().itemsize
        for cfg in conv_configs(
            sympy_product([x.get_size()[0], *x.get_size()[2:]]),
            out_chan,
            in_chan,
            dtype_size=dtype_size,
        ):
            if ndim == 2:
                conv2d_template.maybe_append_choice(
                    choices,
                    input_nodes=(x, weight),
                    layout=layout,
                    KERNEL_H=kernel_shape[0],
                    KERNEL_W=kernel_shape[1],
                    STRIDE_H=stride[0],
                    STRIDE_W=stride[1],
                    PADDING_H=padding[0],
                    PADDING_W=padding[1],
                    GROUPS=groups,
                    # TODO(jansel): try unroll for bigger kernels once fixed:
                    #               https://github.com/triton-lang/triton/issues/1254
                    UNROLL=is_ones(kernel_shape),
                    ALLOW_TF32=torch.backends.cudnn.fp32_precision == "tf32",
                    num_stages=cfg.num_stages,
                    num_warps=cfg.num_warps,
                    **cfg.kwargs,
                )
            elif ndim == 3:
                conv3d_template.maybe_append_choice(
                    choices,
                    input_nodes=(x, weight),
                    layout=layout,
                    KERNEL_D=kernel_shape[0],
                    KERNEL_H=kernel_shape[1],
                    KERNEL_W=kernel_shape[2],
                    STRIDE_D=stride[0],
                    STRIDE_H=stride[1],
                    STRIDE_W=stride[2],
                    PADDING_D=padding[0],
                    PADDING_H=padding[1],
                    PADDING_W=padding[2],
                    GROUPS=groups,
                    # TODO(jansel): try unroll for bigger kernels once fixed:
                    #               https://github.com/triton-lang/triton/issues/1254
                    UNROLL=is_ones(kernel_shape),
                    ALLOW_TF32=torch.backends.cudnn.fp32_precision == "tf32",
                    num_stages=cfg.num_stages,
                    num_warps=cfg.num_warps,
                    **cfg.kwargs,
                )
    if use_ck_conv_template(layout):
        CKGroupedConvFwdTemplate.add_ck_conv_choices(
            choices,
            layout,
            input_nodes=(x, weight) + ((bias,) if bias is not None else tuple()),
            stride=stride,
            padding=padding,
            dilation=dilation,
            groups=groups,
            n_spatial_dimensions=ndim,
        )
    node, _ = autotune_select_algorithm("convolution", choices, args, layout)
    return node


def convolution(
    g: jit_utils.GraphContext,
    input,
    weight,
    bias,
    stride,
    padding,
    dilation,
    transposed,
    output_padding,
    groups,
):
    return _convolution(
        g,
        input,
        weight,
        bias,
        stride,
        padding,
        dilation,
        transposed,
        output_padding,
        groups,
        None,
        None,
        None,
        None,
    )


def convolution(a, b, cycle=0, dps=None, prime=None, dyadic=None, subset=None):
    """
    Performs convolution by determining the type of desired
    convolution using hints.

    Exactly one of ``dps``, ``prime``, ``dyadic``, ``subset`` arguments
    should be specified explicitly for identifying the type of convolution,
    and the argument ``cycle`` can be specified optionally.

    For the default arguments, linear convolution is performed using **FFT**.

    Parameters
    ==========

    a, b : iterables
        The sequences for which convolution is performed.
    cycle : Integer
        Specifies the length for doing cyclic convolution.
    dps : Integer
        Specifies the number of decimal digits for precision for
        performing **FFT** on the sequence.
    prime : Integer
        Prime modulus of the form `(m 2^k + 1)` to be used for
        performing **NTT** on the sequence.
    dyadic : bool
        Identifies the convolution type as dyadic (*bitwise-XOR*)
        convolution, which is performed using **FWHT**.
    subset : bool
        Identifies the convolution type as subset convolution.

    Examples
    ========

    >>> from sympy import convolution, symbols, S, I
    >>> u, v, w, x, y, z = symbols('u v w x y z')

    >>> convolution([1 + 2*I, 4 + 3*I], [S(5)/4, 6], dps=3)
    [1.25 + 2.5*I, 11.0 + 15.8*I, 24.0 + 18.0*I]
    >>> convolution([1, 2, 3], [4, 5, 6], cycle=3)
    [31, 31, 28]

    >>> convolution([111, 777], [888, 444], prime=19*2**10 + 1)
    [1283, 19351, 14219]
    >>> convolution([111, 777], [888, 444], prime=19*2**10 + 1, cycle=2)
    [15502, 19351]

    >>> convolution([u, v], [x, y, z], dyadic=True)
    [u*x + v*y, u*y + v*x, u*z, v*z]
    >>> convolution([u, v], [x, y, z], dyadic=True, cycle=2)
    [u*x + u*z + v*y, u*y + v*x + v*z]

    >>> convolution([u, v, w], [x, y, z], subset=True)
    [u*x, u*y + v*x, u*z + w*x, v*z + w*y]
    >>> convolution([u, v, w], [x, y, z], subset=True, cycle=3)
    [u*x + v*z + w*y, u*y + v*x, u*z + w*x]

    """

    c = as_int(cycle)
    if c < 0:
        raise ValueError("The length for cyclic convolution "
                        "must be non-negative")

    dyadic = True if dyadic else None
    subset = True if subset else None
    if sum(x is not None for x in (prime, dps, dyadic, subset)) > 1:
        raise TypeError("Ambiguity in determining the type of convolution")

    if prime is not None:
        ls = convolution_ntt(a, b, prime=prime)
        return ls if not c else [sum(ls[i::c]) % prime for i in range(c)]

    if dyadic:
        ls = convolution_fwht(a, b)
    elif subset:
        ls = convolution_subset(a, b)
    else:
        def loop(a):
            dens = []
            for i in a:
                if isinstance(i, Rational) and i.q - 1:
                    dens.append(i.q)
                elif not isinstance(i, int):
                    return
            if dens:
                l = lcm(*dens)
                return [i*l if type(i) is int else i.p*(l//i.q) for i in a], l
            # no lcm of den to deal with
            return a, 1
        ls = None
        da = loop(a)
        if da is not None:
            db = loop(b)
            if db is not None:
                (ia, ma), (ib, mb) = da, db
                den = ma*mb
                ls = convolution_int(ia, ib)
                if den != 1:
                    ls = [Rational(i, den) for i in ls]
        if ls is None:
            ls = convolution_fft(a, b, dps)

    return ls if not c else [sum(ls[i::c]) for i in range(c)]


def convolution(result: _ods_ir.Type, lhs: _ods_ir.Value[_ods_ir.RankedTensorType], rhs: _ods_ir.Value[_ods_ir.RankedTensorType], dimension_numbers: _Union[_Any, _ods_ir.Attribute], feature_group_count: _Union[int, _ods_ir.IntegerAttr], batch_group_count: _Union[int, _ods_ir.IntegerAttr], *, window_strides: _Optional[_Union[_Union[_Sequence[int], _Buffer], _ods_ir.DenseIntElementsAttr]] = None, padding: _Optional[_Union[_Union[_Sequence[int], _Buffer], _ods_ir.DenseIntElementsAttr]] = None, lhs_dilation: _Optional[_Union[_Union[_Sequence[int], _Buffer], _ods_ir.DenseIntElementsAttr]] = None, rhs_dilation: _Optional[_Union[_Union[_Sequence[int], _Buffer], _ods_ir.DenseIntElementsAttr]] = None, window_reversal: _Optional[_Union[_Any, _ods_ir.DenseElementsAttr]] = None, precision_config: _Optional[_Union[_Any, _ods_ir.ArrayAttr]] = None, loc: _Optional[_ods_ir.Location] = None, ip: _Optional[_ods_ir.InsertionPoint] = None) -> _ods_ir.OpResult[_ods_ir.RankedTensorType]:
  return ConvolutionOp(result=result, lhs=lhs, rhs=rhs, dimension_numbers=dimension_numbers, feature_group_count=feature_group_count, batch_group_count=batch_group_count, window_strides=window_strides, padding=padding, lhs_dilation=lhs_dilation, rhs_dilation=rhs_dilation, window_reversal=window_reversal, precision_config=precision_config, loc=loc, ip=ip).result


def convolution(result: _ods_ir.Type, lhs: _ods_ir.Value[_ods_ir.RankedTensorType], rhs: _ods_ir.Value[_ods_ir.RankedTensorType], dimension_numbers: _Union[_Any, _ods_ir.Attribute], feature_group_count: _Union[int, _ods_ir.IntegerAttr], batch_group_count: _Union[int, _ods_ir.IntegerAttr], *, window_strides: _Optional[_Union[_Sequence[int], _ods_ir.DenseI64ArrayAttr]] = None, padding: _Optional[_Union[_Union[_Sequence[int], _Buffer], _ods_ir.DenseIntElementsAttr]] = None, lhs_dilation: _Optional[_Union[_Sequence[int], _ods_ir.DenseI64ArrayAttr]] = None, rhs_dilation: _Optional[_Union[_Sequence[int], _ods_ir.DenseI64ArrayAttr]] = None, window_reversal: _Optional[_Union[_Sequence[bool], _ods_ir.DenseBoolArrayAttr]] = None, precision_config: _Optional[_Union[_Any, _ods_ir.ArrayAttr]] = None, loc: _Optional[_ods_ir.Location] = None, ip: _Optional[_ods_ir.InsertionPoint] = None) -> _ods_ir.OpResult[_ods_ir.RankedTensorType]:
  return ConvolutionOp(result=result, lhs=lhs, rhs=rhs, dimension_numbers=dimension_numbers, feature_group_count=feature_group_count, batch_group_count=batch_group_count, window_strides=window_strides, padding=padding, lhs_dilation=lhs_dilation, rhs_dilation=rhs_dilation, window_reversal=window_reversal, precision_config=precision_config, loc=loc, ip=ip).result

