from typing import Any

def validateLayerInfoVersion3Data(infoData: dict[str, Any]) -> dict[str, Any]:
    """
    This performs very basic validation of the value for infoData
    following the UFO 3 layerinfo.plist specification. The results
    of this should not be interpretted as *correct* for the font
    that they are part of. This merely indicates that the values
    are of the proper type and, where the specification defines
    a set range of possible values for an attribute, that the
    value is in the accepted range.
    """
    for attr, value in infoData.items():
        if attr not in layerInfoVersion3ValueData:
            raise GlifLibError("Unknown attribute %s." % attr)
        isValidValue = validateLayerInfoVersion3ValueForAttribute(attr, value)
        if not isValidValue:
            raise GlifLibError(f"Invalid value for attribute {attr} ({value!r}).")
    return infoData

