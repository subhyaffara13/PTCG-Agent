
def glyph_to_quadratic(glyph, **kwargs):
    """Convenience wrapper around glyphs_to_quadratic, for just one glyph.
    Return True if the glyph was modified, else return False.
    """

    return glyphs_to_quadratic([glyph], **kwargs)

