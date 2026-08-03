from typing import Any

def convertFontInfoValueForAttributeFromVersion2ToVersion1(
    attr: str, value: Any
) -> tuple[str, Any]:
    """
    Convert value from version 2 to version 1 format.
    Returns the new attribute name and the converted value.
    If the value is None, None will be returned for the new value.
    """
    if value is not None:
        if attr == "styleMapStyleName":
            value = _fontStyle2To1.get(value)
        elif attr == "openTypeOS2WidthClass":
            value = _widthName2To1.get(value)
        elif attr == "postscriptWindowsCharacterSet":
            value = _msCharSet2To1.get(value)
    attr = fontInfoAttributesVersion2To1.get(attr, attr)
    return attr, value

