
def native_group_norm(
    input: Tensor,
    weight: Tensor | None,
    bias: Tensor | None,
    batch_size: int,
    num_channels: int,
    flattened_inner_size: int,
    num_groups: int,
    eps: float,
) -> tuple[Tensor, Tensor, Tensor]:
    torch._check(
        input.ndim >= 2,
        lambda: f"Expected at least 2 dimensions for input tensor but received {input.ndim}",
    )
    torch._check(
        num_channels % num_groups == 0,
        lambda: "Expected number of channels in input to be divisible by num_groups, "
        + f"but got input of shape {input.shape} and num_groups = {num_groups}",
    )

    computation_dtype = utils.get_computation_dtype(input.dtype)
    input_acc = _maybe_convert_to_dtype(input, computation_dtype)
    # num_channels / num_groups and flattened inner dimension are the reduction axes
    reduction_dims = [2, 3]
    input_reshaped = torch.reshape(
        input_acc,
        [batch_size, num_groups, num_channels // num_groups, flattened_inner_size],
    )
    reduction_dims = utils.canonicalize_dims(input_reshaped.ndim, reduction_dims)
    biased_var, mean = torch.var_mean(
        input_reshaped, dim=reduction_dims, unbiased=False, keepdim=True
    )
    rstd = torch.rsqrt(biased_var + eps)
    if input.device.type == "cpu" and weight is not None:
        weight_reshaped = torch.reshape(
            weight, [1, num_groups, num_channels // num_groups, 1]
        )
        w = rstd * weight_reshaped
        b = -mean * w
        if bias is not None:
            bias_reshaped = torch.reshape(
                bias, [1, num_groups, num_channels // num_groups, 1]
            )
            b = b + bias_reshaped
        w = w.contiguous().as_strided([batch_size, num_channels], [num_channels, 1])
        b = b.contiguous().as_strided([batch_size, num_channels], [num_channels, 1])
        broadcast_dims = list(range(2, input.ndim))
        unsqueeze_w = _unsqueeze_multiple(w, broadcast_dims)
        unsqueeze_b = _unsqueeze_multiple(b, broadcast_dims)
        out = input_acc * unsqueeze_w + unsqueeze_b
    else:
        out = (input_reshaped - mean) * rstd
        out = out.view(input.shape)
        broadcast_dims = [0] + list(range(2, input.ndim))
        if weight is not None:
            unsqueeze_weight = _unsqueeze_multiple(weight, broadcast_dims)
            out = out * unsqueeze_weight
        if bias is not None:
            unsqueeze_bias = _unsqueeze_multiple(bias, broadcast_dims)
            out = out + unsqueeze_bias

    out = _maybe_convert_to_dtype(out, input.dtype)  # type: ignore[assignment]
    mean = _maybe_convert_to_dtype(mean, input.dtype)  # type: ignore[assignment]
    rstd = _maybe_convert_to_dtype(rstd, input.dtype)  # type: ignore[assignment]

    # remove broadcast dimensions from mean and rstd
    mean = torch.squeeze(mean, reduction_dims)
    rstd = torch.squeeze(rstd, reduction_dims)
    return (out, mean, rstd)

