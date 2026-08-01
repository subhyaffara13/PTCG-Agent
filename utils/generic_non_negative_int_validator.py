
def genericNonNegativeIntValidator(value: Any) -> bool:
    """
    Generic. (Added at version 3.)
    """
    if not isinstance(value, int):
        return False
    if value < 0:
        return False
    return True

