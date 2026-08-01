
def _check_base_glyphs_exist(colorGlyphs, glyphMap, where):
    """Checks that every base glyph name in colorGlyphs exists in glyphMap."""

    missing = []
    for baseGlyph in colorGlyphs.keys():
        if baseGlyph not in glyphMap:
            missing.append(baseGlyph)

    if missing:
        preview = ", ".join(missing[:10])
        extra = ""
        if len(missing) > 10:
            extra = f" (and {len(missing) - 10} more)"
        raise ColorLibError(
            f"{where}: base glyph(s) not found in glyphMap: {preview}{extra}"
        )

