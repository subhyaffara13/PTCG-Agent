
def fontInfoVersion2OpenTypeOS2PanoseValidator(values: Any) -> bool:
    """
    Version 2.
    """
    if not isinstance(values, (list, tuple)):
        return False
    if len(values) != 10:
        return False
    for value in values:
        if not isinstance(value, int):
            return False
    # XXX further validation?
    return True

