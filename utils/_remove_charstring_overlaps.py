
def _remove_charstring_overlaps(
    *,
    glyphName: str,
    glyphSet: _TTGlyphMapping,
    cffFontSet: CFFFontSet,
) -> bool:
    path = skPathFromGlyph(glyphName, glyphSet)

    # remove overlaps
    path2 = _simplify(path, glyphName, round=noRound)

    # replace TTGlyph if simplified path is different (ignoring contour order)
    if not _same_path(path, path2):
        charStrings = cffFontSet[0].CharStrings
        charStrings[glyphName] = _charString_from_SkPath(path2, charStrings[glyphName])
        return True

    return False

