
def parseAttachList(lines, font):
    points = {}
    with lines.between("attachment list"):
        for line in lines:
            glyph = makeGlyph(line[0])
            assert glyph not in points, glyph
            points[glyph] = [int(i) for i in line[1:]]
    return otl.buildAttachList(points, font.getReverseGlyphMap())

