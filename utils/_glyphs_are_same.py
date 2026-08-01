
def _glyphsAreSame(
    glyphSet1,
    glyphSet2,
    glyph1,
    glyph2,
    advanceTolerance=0.05,
    advanceToleranceEmpty=0.20,
):
    pen1 = DecomposingRecordingPen(glyphSet1)
    pen2 = DecomposingRecordingPen(glyphSet2)
    g1 = glyphSet1[glyph1]
    g2 = glyphSet2[glyph2]
    g1.draw(pen1)
    g2.draw(pen2)
    if pen1.value != pen2.value:
        return False
    # Allow more width tolerance for glyphs with no ink
    tolerance = advanceTolerance if pen1.value else advanceToleranceEmpty
    # TODO Warn if advances not the same but within tolerance.
    if abs(g1.width - g2.width) > g1.width * tolerance:
        return False
    if hasattr(g1, "height") and g1.height is not None:
        if abs(g1.height - g2.height) > g1.height * tolerance:
            return False
    return True

