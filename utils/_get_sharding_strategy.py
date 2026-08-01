
def _get_sharding_strategy(handle):
    """
    Returns the sharding strategy of the handle.
    """
    return handle._sharding_strategy if handle else None

