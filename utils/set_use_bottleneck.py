
def set_use_bottleneck(v: bool = True) -> None:
    # set/unset to use bottleneck
    global _USE_BOTTLENECK
    if _BOTTLENECK_INSTALLED:
        _USE_BOTTLENECK = v

