from typing import Any

def anchorValidator(value: Any) -> bool:
    """
    Version 3+.
    """
    if not genericDictValidator(value, _anchorDictPrototype):
        return False
    x = value.get("x")
    y = value.get("y")
    # x and y must be present
    if x is None or y is None:
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

