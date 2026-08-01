
def drop_implied_oncurve_points(*masters: TTFont) -> int:
    """Drop impliable on-curve points from all the simple glyphs in masters.

    In TrueType glyf outlines, on-curve points can be implied when they are located
    exactly at the midpoint of the line connecting two consecutive off-curve points.

    The input masters' glyf tables are assumed to contain same-named glyphs that are
    interpolatable. Oncurve points are only dropped if they can be implied for all
    the masters. The fonts are modified in-place.

    Args:
        masters: The TTFont(s) to modify

    Returns:
        The total number of points that were dropped if any.

    Reference:
    https://developer.apple.com/fonts/TrueType-Reference-Manual/RM01/Chap1.html
    """

    glyph_masters = defaultdict(list)
    # multiple DS source may point to the same TTFont object and we want to
    # avoid processing the same glyph twice as they are modified in-place
    for font in {id(m): m for m in masters}.values():
        glyf = font["glyf"]
        for glyphName in glyf.keys():
            glyph_masters[glyphName].append(glyf[glyphName])
    count = 0
    for glyphName, glyphs in glyph_masters.items():
        try:
            dropped = dropImpliedOnCurvePoints(*glyphs)
        except ValueError as e:
            # we don't fail for incompatible glyphs in _add_gvar so we shouldn't here
            log.warning("Failed to drop implied oncurves for %r: %s", glyphName, e)
        else:
            count += len(dropped)
    return count

