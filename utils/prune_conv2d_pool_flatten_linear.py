
def prune_conv2d_pool_flatten_linear(
    conv2d: nn.Conv2d,
    pool: nn.Module,
    flatten: Callable[[Tensor], Tensor] | None,
    linear: nn.Linear,
) -> None:
    mask = _prune_conv2d_helper(conv2d)

    # We map the pruned indices of the Conv2d output to the flattened indices of the Linear following the Flatten layer.
    # we determine the flattening scale (h * w), and readjust `first_pruned_indices`
    # (each idx maps to range idx * h * w to (idx+1) * h * w), `first_valid_indices`,
    # and `pruned_biases` (repeat each bias by h * w).
    if parametrize.is_parametrized(linear):
        parametrization_dict = cast(nn.ModuleDict, linear.parametrizations)
        weight_parameterizations = cast(
            ParametrizationList, parametrization_dict.weight
        )
        linear_ic = weight_parameterizations.original.shape[1]
    else:
        linear_ic = linear.weight.shape[1]

    conv2d_oc = len(mask)
    if linear_ic % conv2d_oc != 0:
        raise AssertionError(
            f"Flattening from dimensions {conv2d_oc} to {linear_ic} not supported"
        )

    flatten_scale = linear_ic // conv2d_oc
    flattened_mask = torch.tensor(
        [[val] * flatten_scale for val in mask], dtype=torch.bool, device=mask.device
    ).flatten()

    if getattr(conv2d, "prune_bias", False):
        _prune_module_bias(conv2d, mask)
    else:
        pruned_biases = cast(Tensor, _propagate_module_bias(conv2d, mask))
        flattened_pruned_biases = torch.tensor(
            [[bias] * flatten_scale for bias in pruned_biases], device=mask.device
        ).flatten()
        linear.bias = _get_adjusted_next_layer_bias(
            linear, flattened_pruned_biases, flattened_mask
        )

    with torch.no_grad():
        if parametrize.is_parametrized(linear):
            parametrization_dict = cast(nn.ModuleDict, linear.parametrizations)
            weight_parameterizations = cast(
                ParametrizationList, parametrization_dict.weight
            )
            weight_parameterizations.original = nn.Parameter(
                weight_parameterizations.original[:, flattened_mask]
            )
            linear.in_features = weight_parameterizations.original.shape[1]
        else:
            linear.weight = nn.Parameter(linear.weight[:, flattened_mask])
            linear.in_features = linear.weight.shape[1]

