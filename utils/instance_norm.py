
def instance_norm(
    input: Tensor,
    running_mean: Tensor | None = None,
    running_var: Tensor | None = None,
    weight: Tensor | None = None,
    bias: Tensor | None = None,
    use_input_stats: bool = True,
    momentum: float = 0.1,
    eps: float = 1e-5,
) -> Tensor:
    r"""Apply Instance Normalization independently for each channel in every data sample within a batch.

    See :class:`~torch.nn.InstanceNorm1d`, :class:`~torch.nn.InstanceNorm2d`,
    :class:`~torch.nn.InstanceNorm3d` for details.
    """
    if has_torch_function_variadic(input, running_mean, running_var, weight, bias):
        return handle_torch_function(
            instance_norm,
            (input, running_mean, running_var, weight, bias),
            input,
            running_mean=running_mean,
            running_var=running_var,
            weight=weight,
            bias=bias,
            use_input_stats=use_input_stats,
            momentum=momentum,
            eps=eps,
        )
    if use_input_stats:
        # pyrefly: ignore [bad-argument-type]
        _verify_spatial_size(input.size())
    return torch.instance_norm(
        input,
        weight,
        bias,
        running_mean,
        running_var,
        use_input_stats,
        momentum,
        eps,
        torch.backends.cudnn.enabled,
    )


def instance_norm(
    g: jit_utils.GraphContext,
    input,
    weight,
    bias,
    running_mean,
    running_var,
    use_input_stats: bool,
    momentum: Number,
    eps: Number,
    cudnn_enabled: bool,
):
    symbolic_helper.check_training_mode(use_input_stats, "instance_norm")
    channel_size = symbolic_helper._get_tensor_dim_size(input, 1)
    if weight is None or symbolic_helper._is_none(weight):
        if channel_size is None:
            raise errors.SymbolicValueError(
                "Unsupported: ONNX export of instance_norm for unknown channel size.",
                input,
            )
        weight_value = torch.tensor(
            [1.0] * channel_size,
            dtype=_type_utils.JitScalarType.from_value(input).dtype(),
        )
        weight = g.op("Constant", value_t=weight_value)
    if bias is None or symbolic_helper._is_none(bias):
        if channel_size is None:
            raise errors.SymbolicValueError(
                "Unsupported: ONNX export of instance_norm for unknown channel size.",
                input,
            )
        bias_value = torch.tensor(
            [0.0] * channel_size,
            dtype=_type_utils.JitScalarType.from_value(input).dtype(),
        )
        bias = g.op("Constant", value_t=bias_value)
    if (
        running_mean is None
        or symbolic_helper._is_none(running_mean)
        or running_var is None
        or symbolic_helper._is_none(running_var)
    ):
        return g.op("InstanceNormalization", input, weight, bias, epsilon_f=eps)
    else:
        input_size = symbolic_helper._get_tensor_sizes(input)
        # If input shape is [N, C, H, W], reshape to [1, N * C, H, W] and call batch_norm.
        # For more information instance_norm():
        # https://github.com/pytorch/pytorch/blob/master/aten/src/ATen/native/Normalization.cpp#L542
        input_size_reshape = input_size.copy()
        n = input_size[0]
        if n is None:
            raise errors.SymbolicValueError(
                "Unsupported: ONNX export of instance_norm training for unknown "
                "batch size.",
                input,
            )
        c = input_size[1]
        input_size_reshape[0] = 1
        input_size_reshape[1] = n * c
        weight_ = repeat(
            g, weight, g.op("Constant", value_t=torch.tensor([n], dtype=torch.int64))
        )
        bias_ = repeat(
            g, bias, g.op("Constant", value_t=torch.tensor([n], dtype=torch.int64))
        )
        running_mean_ = repeat(
            g,
            running_mean,
            g.op("Constant", value_t=torch.tensor([n], dtype=torch.int64)),
        )
        running_var_ = repeat(
            g,
            running_var,
            g.op("Constant", value_t=torch.tensor([n], dtype=torch.int64)),
        )
        input_reshaped = g.op(
            "Reshape",
            input,
            g.op("Constant", value_t=torch.LongTensor(input_size_reshape)),
        )
        out = batch_norm(
            g,
            input_reshaped,
            weight_,
            bias_,
            running_mean_,
            running_var_,
            use_input_stats,
            momentum,
            eps,
            cudnn_enabled,
        )
        return view(g, out, g.op("Constant", value_t=torch.tensor(input_size)))

