
def parseSingleSubst(lines, font, _lookupMap=None):
    mapping = {}
    for line in lines:
        assert len(line) == 2, line
        line = makeGlyphs(line)
        mapping[line[0]] = line[1]
    return otl.buildSingleSubstSubtable(mapping)

