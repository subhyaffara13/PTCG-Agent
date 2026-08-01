
def fontInfoWOFFMetadataExtensionItemValidator(value: Any) -> bool:
    """
    Version 3+.
    """
    dictPrototype: GenericDict = dict(
        id=(str, False), names=(list, True), values=(list, True)
    )
    if not genericDictValidator(value, dictPrototype):
        return False
    for name in value["names"]:
        if not fontInfoWOFFMetadataExtensionNameValidator(name):
            return False
    for val in value["values"]:
        if not fontInfoWOFFMetadataExtensionValueValidator(val):
            return False
    return True

