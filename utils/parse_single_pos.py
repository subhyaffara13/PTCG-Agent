
def parseSinglePos(lines, font, _lookupMap=None):
    values = {}
    for line in lines:
        assert len(line) == 3, line
        w = line[0].title().replace(" ", "")
        assert w in valueRecordFormatDict
        g = makeGlyph(line[1])
        v = int(line[2])
        if g not in values:
            values[g] = ValueRecord()
        assert not hasattr(values[g], w), (g, w)
        setattr(values[g], w, v)
    return otl.buildSinglePosSubtable(values, font.getReverseGlyphMap())

