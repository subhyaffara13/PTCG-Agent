
def _prune_conv2d_helper(conv2d: nn.Conv2d) -> Tensor:
    parametrization_dict = cast(nn.ModuleDict, conv2d.parametrizations)
    weight_parameterizations = cast(ParametrizationList, parametrization_dict.weight)
    for p in weight_parameterizations:
        if isinstance(p, FakeStructuredSparsity):
            mask = cast(Tensor, p.mask)

    with torch.no_grad():
        parametrize.remove_parametrizations(conv2d, "weight", leave_parametrized=True)
        conv2d.weight = nn.Parameter(conv2d.weight[mask])  # type: ignore[possibly-undefined]
    conv2d.out_channels = conv2d.weight.shape[0]

    _remove_bias_handles(conv2d)
    # pyrefly: ignore [unbound-name]
    return mask

