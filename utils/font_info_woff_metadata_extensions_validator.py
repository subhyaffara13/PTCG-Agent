
def fontInfoWOFFMetadataExtensionsValidator(value: Any) -> bool:
    """
    Version 3+.
    """
    if not isinstance(value, list):
        return False
    if not value:
        return False
    for extension in value:
        if not fontInfoWOFFMetadataExtensionValidator(extension):
            return False
    return True

