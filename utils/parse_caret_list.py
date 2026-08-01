
def parseCaretList(lines, font):
    carets = {}
    with lines.between("carets"):
        for line in lines:
            glyph = makeGlyph(line[0])
            assert glyph not in carets, glyph
            num = int(line[1])
            thisCarets = [int(i) for i in line[2:]]
            assert num == len(thisCarets), line
            carets[glyph] = thisCarets
    return otl.buildLigCaretList(carets, {}, font.getReverseGlyphMap())

