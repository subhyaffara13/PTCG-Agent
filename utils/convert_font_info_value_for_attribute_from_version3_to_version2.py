
def convertFontInfoValueForAttributeFromVersion3ToVersion2(
    attr: str, value: Any
) -> tuple[str, Any]:
    """
    Convert value from version 3 to version 2 format.
    Returns the new attribute name and the converted value.
    If the value is None, None will be returned for the new value.
    """
    return attr, value

