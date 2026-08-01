
def parseLigature(lines, font, _lookupMap=None):
    mapping = {}
    for line in lines:
        assert len(line) >= 2, line
        line = makeGlyphs(line)
        mapping[tuple(line[1:])] = line[0]
    return otl.buildLigatureSubstSubtable(mapping)

