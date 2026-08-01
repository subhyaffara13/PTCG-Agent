
def prune_linear(linear: nn.Linear) -> None:
    mask = _prune_linear_helper(linear)
    if getattr(linear, "prune_bias", False):
        _prune_module_bias(linear, mask)

