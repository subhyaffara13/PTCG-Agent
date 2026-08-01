
def fontInfoOpenTypeOS2WidthClassValidator(value: Any) -> bool:
    """
    Version 2+.
    """
    if not isinstance(value, int):
        return False
    if value < 1:
        return False
    if value > 9:
        return False
    return True

