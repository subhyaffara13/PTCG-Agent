
def set_sharing_strategy(new_strategy):
    """Set the strategy for sharing CPU tensors.

    Args:
        new_strategy (str): Name of the selected strategy. Should be one of
            the values returned by :func:`get_all_sharing_strategies()`.
    """
    global _sharing_strategy
    if new_strategy not in _all_sharing_strategies:
        raise AssertionError(
            f"invalid sharing strategy {new_strategy!r}, "
            f"expected one of {_all_sharing_strategies}"
        )
    _sharing_strategy = new_strategy

