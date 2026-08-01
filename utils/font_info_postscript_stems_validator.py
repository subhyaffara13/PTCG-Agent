
def fontInfoPostscriptStemsValidator(values: Any) -> bool:
    """
    Version 2+.
    """
    if not isinstance(values, (list, tuple)):
        return False
    if len(values) > 12:
        return False
    for value in values:
        if not isinstance(value, numberTypes):
            return False
    return True

