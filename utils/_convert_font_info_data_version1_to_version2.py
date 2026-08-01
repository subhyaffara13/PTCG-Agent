
def _convertFontInfoDataVersion1ToVersion2(data: dict[str, Any]) -> dict[str, Any]:
    converted = {}
    for attr, value in list(data.items()):
        # FontLab gives -1 for the weightValue
        # for fonts wil no defined value. Many
        # format version 1 UFOs will have this.
        if attr == "weightValue" and value == -1:
            continue
        newAttr, newValue = convertFontInfoValueForAttributeFromVersion1ToVersion2(
            attr, value
        )
        # skip if the attribute is not part of version 2
        if newAttr not in fontInfoAttributesVersion2:
            continue
        # catch values that can't be converted
        if value is None:
            raise UFOLibError(
                f"Cannot convert value ({value!r}) for attribute {newAttr}."
            )
        # store
        converted[newAttr] = newValue
    return converted

