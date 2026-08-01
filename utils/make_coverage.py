
def makeCoverage(glyphs, font, klass=ot.Coverage):
    if not glyphs:
        return None
    if isinstance(glyphs, set):
        glyphs = sorted(glyphs)
    coverage = klass()
    coverage.glyphs = sorted(set(glyphs), key=font.getGlyphID)
    return coverage

