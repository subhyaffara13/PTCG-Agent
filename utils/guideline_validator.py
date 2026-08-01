
def guidelineValidator(value: Any) -> bool:
    """
    Version 3+.
    """
    if not genericDictValidator(value, _guidelineDictPrototype):
        return False

    angle = value.get("angle")
    # angle must be between 0 and 360
    if angle is not None:
        if angle < 0:
            return False
        if angle > 360:
            return False
    # identifier must be 1 or more characters
    identifier = value.get("identifier")
    if identifier is not None and not identifierValidator(identifier):
        return False
    # color must follow the proper format
    color = value.get("color")
    if color is not None and not colorValidator(color):
        return False
    return True

