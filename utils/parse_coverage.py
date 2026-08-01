
def parseCoverage(lines, font, klass=ot.Coverage):
    glyphs = []
    with lines.between("coverage definition"):
        for line in lines:
            glyphs.append(makeGlyph(line[0]))
    return makeCoverage(glyphs, font, klass)

