
def _prune_module_bias(module: nn.Module, mask: Tensor) -> None:
    r"""Applies mask to given modules bias"""
    # prune bias along with weights, discard pruned indices of bias
    original_bias = cast(Tensor, getattr(module, "_bias", module.bias))
    if original_bias is not None:
        module.bias = nn.Parameter(original_bias[mask])

    #  remove _bias parameter
    if hasattr(module, "_bias"):
        delattr(module, "_bias")

