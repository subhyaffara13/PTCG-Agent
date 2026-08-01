
def _prune_linear_helper(linear: nn.Linear) -> Tensor:
    # expects linear to be a parameterized linear module
    parametrization_dict = cast(nn.ModuleDict, linear.parametrizations)
    weight_parameterizations = cast(ParametrizationList, parametrization_dict.weight)
    for p in weight_parameterizations:
        if isinstance(p, FakeStructuredSparsity):
            mask = cast(Tensor, p.mask)

    with torch.no_grad():
        parametrize.remove_parametrizations(linear, "weight", leave_parametrized=True)
        linear.weight = nn.Parameter(linear.weight[mask])  # type: ignore[possibly-undefined]
    linear.out_features = linear.weight.shape[0]
    _remove_bias_handles(linear)

    # pyrefly: ignore [unbound-name]
    return mask

