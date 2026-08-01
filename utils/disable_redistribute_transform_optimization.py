
def disable_redistribute_transform_optimization(disabled: bool = True):
    """
    Context manager to disable the transform optimization pass that merges
    consecutive same-type collectives into single flattened operations.

    When the optimization is disabled, ``_optimize_transform_infos`` becomes a
    no-op and returns the original list of ``_TransformInfo`` objects unchanged.
    This is useful for debugging or isolating issues related to the flattened
    collective merging logic.

    The flag can also be set directly::

        torch.distributed.tensor._redistribute._DISABLE_REDISTRIBUTE_TRANSFORM_OPTIMIZATION = True

    Args:
        disabled (bool): If True (default), disables the optimization.
                         If False, explicitly enables it (the normal default).
    """
    global _DISABLE_REDISTRIBUTE_TRANSFORM_OPTIMIZATION

    old_value = _DISABLE_REDISTRIBUTE_TRANSFORM_OPTIMIZATION
    _DISABLE_REDISTRIBUTE_TRANSFORM_OPTIMIZATION = disabled
    try:
        yield
    finally:
        _DISABLE_REDISTRIBUTE_TRANSFORM_OPTIMIZATION = old_value

