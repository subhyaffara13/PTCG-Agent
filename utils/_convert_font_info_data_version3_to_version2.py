from typing import Any

def _convertFontInfoDataVersion3ToVersion2(data: dict[str, Any]) -> dict[str, Any]:
    converted = {}
    for attr, value in list(data.items()):
        newAttr, newValue = convertFontInfoValueForAttributeFromVersion3ToVersion2(
            attr, value
        )
        if newAttr not in fontInfoAttributesVersion2:
            continue
        converted[newAttr] = newValue
    return converted

