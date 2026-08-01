
def _convertFontInfoDataVersion2ToVersion1(data: dict[str, Any]) -> dict[str, Any]:
    converted = {}
    for attr, value in list(data.items()):
        newAttr, newValue = convertFontInfoValueForAttributeFromVersion2ToVersion1(
            attr, value
        )
        # only take attributes that are registered for version 1
        if newAttr not in fontInfoAttributesVersion1:
            continue
        # catch values that can't be converted
        if value is None:
            raise UFOLibError(
                f"Cannot convert value ({value!r}) for attribute {newAttr}."
            )
        # store
        converted[newAttr] = newValue
    return converted

