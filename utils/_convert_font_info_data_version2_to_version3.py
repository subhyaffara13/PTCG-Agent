from typing import Any

def _convertFontInfoDataVersion2ToVersion3(data: dict[str, Any]) -> dict[str, Any]:
    converted = {}
    for attr, value in list(data.items()):
        attr, value = convertFontInfoValueForAttributeFromVersion2ToVersion3(
            attr, value
        )
        converted[attr] = value
    return converted

