
def is_dunder(name: str, exclude_special: bool = False) -> bool:
    """Returns whether name is a dunder name.

    Args:
        exclude_special: Whether to return False for a couple special dunder methods.

    """
    if exclude_special and name in SPECIAL_DUNDERS:
        return False
    return name.startswith("__") and name.endswith("__")

