
def removeTTGlyphOverlaps(
    glyphName: str,
    glyphSet: _TTGlyphMapping,
    glyfTable: _g_l_y_f.table__g_l_y_f,
    hmtxTable: _h_m_t_x.table__h_m_t_x,
    removeHinting: bool = True,
) -> bool:
    glyph = glyfTable[glyphName]
    # decompose composite glyphs only if components overlap each other
    if (
        glyph.numberOfContours > 0
        or glyph.isComposite()
        and componentsOverlap(glyph, glyphSet)
    ):
        path = skPathFromGlyph(glyphName, glyphSet)

        # remove overlaps
        path2 = _simplify(path, glyphName)

        # replace TTGlyph if simplified path is different (ignoring contour order)
        if not _same_path(path, path2):
            glyfTable[glyphName] = glyph = ttfGlyphFromSkPath(path2)
            # simplified glyph is always unhinted
            assert not glyph.program
            # also ensure hmtx LSB == glyph.xMin so glyph origin is at x=0
            width, lsb = hmtxTable[glyphName]
            if lsb != glyph.xMin:
                hmtxTable[glyphName] = (width, glyph.xMin)
            return True

    if removeHinting:
        glyph.removeHinting()
    return False

