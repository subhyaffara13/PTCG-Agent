
def _bounds(font):
    """
    Compute the font bounding box, as if all glyphs were written
    at the same start position.

    Helper function for _font_to_ps_type42.

    Parameters
    ----------
    font : fontTools.ttLib.ttFont.TTFont
        The font

    Returns
    -------
    tuple
        (xMin, yMin, xMax, yMax) of the combined bounding box
        of all the glyphs in the font
    """
    gs = font.getGlyphSet(False)
    pen = fontTools.pens.boundsPen.BoundsPen(gs)
    for name in gs.keys():
        gs[name].draw(pen)
    return pen.bounds or (0, 0, 0, 0)

