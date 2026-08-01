
def _isRibbi(nametable, nameID):
    englishRecord = nametable.getName(nameID, 3, 1, 0x409)
    return (
        True
        if englishRecord is not None
        and englishRecord.toUnicode() in ("Regular", "Italic", "Bold", "Bold Italic")
        else False
    )

