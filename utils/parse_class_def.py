
def parseClassDef(lines, font, klass=ot.ClassDef):
    classDefs = {}
    with lines.between("class definition"):
        for line in lines:
            glyph = makeGlyph(line[0])
            assert glyph not in classDefs, glyph
            classDefs[glyph] = int(line[1])
    return makeClassDef(classDefs, font, klass)

