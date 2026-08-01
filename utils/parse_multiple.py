
def parseMultiple(lines, font, _lookupMap=None):
    mapping = {}
    for line in lines:
        line = makeGlyphs(line)
        mapping[line[0]] = line[1:]
    return otl.buildMultipleSubstSubtable(mapping)

