
def parseCursive(lines, font, _lookupMap=None):
    records = {}
    for line in lines:
        assert len(line) in [3, 4], line
        idx, klass = {
            "entry": (0, ot.EntryAnchor),
            "exit": (1, ot.ExitAnchor),
        }[line[0]]
        glyph = makeGlyph(line[1])
        if glyph not in records:
            records[glyph] = [None, None]
        assert records[glyph][idx] is None, (glyph, idx)
        records[glyph][idx] = makeAnchor(line[2:], klass)
    return otl.buildCursivePosSubtable(records, font.getReverseGlyphMap())

