
def prune_conv2d(conv2d: nn.Conv2d) -> None:
    mask = _prune_conv2d_helper(conv2d)
    if getattr(conv2d, "prune_bias", False):
        _prune_module_bias(conv2d, mask)

