from typing import Any

def convertFontInfoValueForAttributeFromVersion2ToVersion3(
    attr: str, value: Any
) -> tuple[str, Any]:
    """
    Convert value from version 2 to version 3 format.
    Returns the new attribute name and the converted value.
    If the value is None, None will be returned for the new value.
    """
    if attr in _ufo2To3FloatToInt:
        try:
            value = round(value)
        except (ValueError, TypeError):
            raise UFOLibError("Could not convert value for %s." % attr)
    if attr in _ufo2To3NonNegativeInt:
        try:
            value = int(abs(value))
        except (ValueError, TypeError):
            raise UFOLibError("Could not convert value for %s." % attr)
    elif attr in _ufo2To3NonNegativeIntOrFloat:
        try:
            v = float(abs(value))
        except (ValueError, TypeError):
            raise UFOLibError("Could not convert value for %s." % attr)
        if v == int(v):
            v = int(v)
        if v != value:
            value = v
    return attr, value

