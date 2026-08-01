
def prune_conv2d_padded(conv2d_1: nn.Conv2d) -> None:
    parametrization_dict = cast(nn.ModuleDict, conv2d_1.parametrizations)
    weight_parameterizations = cast(ParametrizationList, parametrization_dict.weight)
    for p in weight_parameterizations:
        if isinstance(p, FakeStructuredSparsity):
            mask = cast(Tensor, p.mask)

    with torch.no_grad():
        parametrize.remove_parametrizations(conv2d_1, "weight", leave_parametrized=True)

    if getattr(conv2d_1, "_bias", None) is not None:
        if (
            conv2d_1.bias is not None
        ):  # conv2d_1 has original bias and bias propagated from previous layer
            new_bias = torch.zeros(conv2d_1.bias.shape)
            new_bias[mask] = conv2d_1.bias[mask]  # type: ignore[possibly-undefined]
            # adjusted bias that to keep in conv2d_1
            # pyrefly: ignore [unbound-name]
            new_bias[~mask] = cast(Tensor, conv2d_1._bias)[~mask]
            # pruned biases that are kept instead of propagated
            conv2d_1.bias = nn.Parameter(new_bias)
        else:  # conv2d_1 has only original bias
            conv2d_1.bias = nn.Parameter(cast(Tensor, conv2d_1._bias))
    else:
        # no original bias, only propagated bias
        if (
            conv2d_1.bias is not None
        ):  # conv2d_1 has bias propagated from previous layer
            conv2d_1.bias.data[~mask] = 0  # type: ignore[possibly-undefined]

    if hasattr(conv2d_1, "_bias"):
        delattr(conv2d_1, "_bias")

