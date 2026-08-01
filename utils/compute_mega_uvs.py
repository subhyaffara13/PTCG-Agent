
def computeMegaUvs(merger, uvsTables):
    """Returns merged UVS subtable (cmap format=14)."""
    uvsDict = {}
    cmap = merger.cmap
    for table in uvsTables:
        for variationSelector, uvsMapping in table.uvsDict.items():
            if variationSelector not in uvsDict:
                uvsDict[variationSelector] = {}
            for unicodeValue, glyphName in uvsMapping:
                if cmap.get(unicodeValue) == glyphName:
                    # this is a default variation
                    glyphName = None
                    # prefer previous glyph id if both fonts defined UVS
                if unicodeValue not in uvsDict[variationSelector]:
                    uvsDict[variationSelector][unicodeValue] = glyphName

    for variationSelector in uvsDict:
        uvsDict[variationSelector] = [*uvsDict[variationSelector].items()]

    return uvsDict

