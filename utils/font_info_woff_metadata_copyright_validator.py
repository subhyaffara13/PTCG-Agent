
def fontInfoWOFFMetadataCopyrightValidator(value: Any) -> bool:
    """
    Version 3+.
    """
    dictPrototype: GenericDict = dict(text=(list, True))
    if not genericDictValidator(value, dictPrototype):
        return False
    for text in value["text"]:
        if not fontInfoWOFFMetadataTextValue(text):
            return False
    return True

