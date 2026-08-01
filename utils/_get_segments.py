
def _get_segments(glyph):
    """Get a glyph's segments as extracted by GetSegmentsPen."""

    pen = GetSegmentsPen()
    # glyph.draw(pen)
    # We can't simply draw the glyph with the pen, but we must initialize the
    # PointToSegmentPen explicitly with outputImpliedClosingLine=True.
    # By default PointToSegmentPen does not outputImpliedClosingLine -- unless
    # last and first point on closed contour are duplicated. Because we are
    # converting multiple glyphs at the same time, we want to make sure
    # this function returns the same number of segments, whether or not
    # the last and first point overlap.
    # https://github.com/googlefonts/fontmake/issues/572
    # https://github.com/fonttools/fonttools/pull/1720
    pointPen = PointToSegmentPen(pen, outputImpliedClosingLine=True)
    glyph.drawPoints(pointPen)
    return pen.segments

