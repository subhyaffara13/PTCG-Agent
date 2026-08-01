
def fontInfoWOFFMetadataUniqueIDValidator(value: Any) -> bool:
    """
    Version 3+.
    """
    dictPrototype: GenericDict = dict(id=(str, True))
    if not genericDictValidator(value, dictPrototype):
        return False
    return True

