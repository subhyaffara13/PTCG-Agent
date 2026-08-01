
def renameCFFCharStrings(merger, glyphOrder, cffTable):
    """Rename topDictIndex charStrings based on glyphOrder."""
    td = cffTable.cff.topDictIndex[0]

    charStrings = {}
    for i, v in enumerate(td.CharStrings.charStrings.values()):
        glyphName = glyphOrder[i]
        charStrings[glyphName] = v
    td.CharStrings.charStrings = charStrings

    td.charset = list(glyphOrder)

