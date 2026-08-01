
def fontInfoWOFFMetadataLicenseValidator(value: Any) -> bool:
    """
    Version 3+.
    """
    dictPrototype: GenericDict = dict(
        url=(str, False), text=(list, False), id=(str, False)
    )
    if not genericDictValidator(value, dictPrototype):
        return False
    if "text" in value:
        for text in value["text"]:
            if not fontInfoWOFFMetadataTextValue(text):
                return False
    return True

