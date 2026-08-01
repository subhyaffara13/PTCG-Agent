
def _is_safe_to_split() -> bool:
    """
    Checks if it is safe to split the any process group in the world.
    This is only safe if the default pg has a bound device id, otherwise
    users must be aware that a pg is only splittable after the first collective is
    issued.
    """
    return _get_default_group().bound_device_id is not None

