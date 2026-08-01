
def convertFontInfoValueForAttributeFromVersion1ToVersion2(
    attr: str, value: Any
) -> tuple[str, Any]:
    """
    Convert value from version 1 to version 2 format.
    Returns the new attribute name and the converted value.
    If the value is None, None will be returned for the new value.
    """
    # convert floats to ints if possible
    if isinstance(value, float):
        if int(value) == value:
            value = int(value)
    if value is not None:
        if attr == "fontStyle":
            v: Optional[Union[str, int]] = _fontStyle1To2.get(value)
            if v is None:
                raise UFOLibError(
                    f"Cannot convert value ({value!r}) for attribute {attr}."
                )
            value = v
        elif attr == "widthName":
            v = _widthName1To2.get(value)
            if v is None:
                raise UFOLibError(
                    f"Cannot convert value ({value!r}) for attribute {attr}."
                )
            value = v
        elif attr == "msCharSet":
            v = _msCharSet1To2.get(value)
            if v is None:
                raise UFOLibError(
                    f"Cannot convert value ({value!r}) for attribute {attr}."
                )
            value = v
    attr = fontInfoAttributesVersion1To2.get(attr, attr)
    return attr, value

