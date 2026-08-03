import re

def _updateUniqueIdNameRecord(varfont, nameIDs, platform):
    nametable = varfont["name"]
    currentRecord = nametable.getName(NameID.UNIQUE_FONT_IDENTIFIER, *platform)
    if not currentRecord:
        return None

    # Check if full name and postscript name are a substring of currentRecord
    for nameID in (NameID.FULL_FONT_NAME, NameID.POSTSCRIPT_NAME):
        nameRecord = nametable.getName(nameID, *platform)
        if not nameRecord:
            continue
        if nameRecord.toUnicode() in currentRecord.toUnicode():
            return currentRecord.toUnicode().replace(
                nameRecord.toUnicode(), nameIDs[nameRecord.nameID]
            )

    # Create a new string since we couldn't find any substrings.
    fontVersion = _fontVersion(varfont, platform)
    achVendID = varfont["OS/2"].achVendID
    # Remove non-ASCII characers and trailing spaces
    vendor = re.sub(r"[^\x00-\x7F]", "", achVendID).strip()
    psName = nameIDs[NameID.POSTSCRIPT_NAME]
    return f"{fontVersion};{vendor};{psName}"

