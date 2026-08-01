
def imageValidator(value):
    """
    Version 3+.
    """
    if not genericDictValidator(value, _imageDictPrototype):
        return False
    # fileName must be one or more characters
    if not value["fileName"]:
        return False
    # color must follow the proper format
    color = value.get("color")
    if color is not None and not colorValidator(color):
        return False
    return True

