
def validateInfoVersion2Data(infoData: dict[str, Any]) -> dict[str, Any]:
    """
    This performs very basic validation of the value for infoData
    following the UFO 2 fontinfo.plist specification. The results
    of this should not be interpretted as *correct* for the font
    that they are part of. This merely indicates that the values
    are of the proper type and, where the specification defines
    a set range of possible values for an attribute, that the
    value is in the accepted range.
    """
    validInfoData = {}
    for attr, value in list(infoData.items()):
        isValidValue = validateFontInfoVersion2ValueForAttribute(attr, value)
        if not isValidValue:
            raise UFOLibError(f"Invalid value for attribute {attr} ({value!r}).")
        else:
            validInfoData[attr] = value
    return validInfoData

