
def _propagate_module_bias(module: nn.Module, mask: Tensor) -> Tensor | None:
    r"""
    In the case that we need to propagate biases, this function will return the biases we need
    """
    # set current module bias
    if module.bias is not None:
        module.bias = nn.Parameter(cast(Tensor, module.bias)[mask])
    elif getattr(module, "_bias", None) is not None:
        # pyrefly: ignore [bad-assignment]
        module.bias = nn.Parameter(cast(Tensor, module._bias)[mask])

    # get pruned biases to propagate to subsequent layer
    if getattr(module, "_bias", None) is not None:
        pruned_biases = cast(Tensor, module._bias)[~mask]
    else:
        pruned_biases = None

    if hasattr(module, "_bias"):
        delattr(module, "_bias")

    return pruned_biases

