from typing import Set

def dropImpliedOnCurvePoints(*interpolatable_glyphs: Glyph) -> Set[int]:
    """Drop impliable on-curve points from the (simple) glyph or glyphs.

    In TrueType glyf outlines, on-curve points can be implied when they are located at
    the midpoint of the line connecting two consecutive off-curve points.

    If more than one glyphs are passed, these are assumed to be interpolatable masters
    of the same glyph impliable, and thus only the on-curve points that are impliable
    for all of them will actually be implied.
    Composite glyphs or empty glyphs are skipped, only simple glyphs with 1 or more
    contours are considered.
    The input glyph(s) is/are modified in-place.

    Args:
        interpolatable_glyphs: The glyph or glyphs to modify in-place.

    Returns:
        The set of point indices that were dropped if any.

    Raises:
        ValueError if simple glyphs are not in fact interpolatable because they have
        different point flags or number of contours.

    Reference:
    https://developer.apple.com/fonts/TrueType-Reference-Manual/RM01/Chap1.html
    """
    staticAttributes = SimpleNamespace(
        numberOfContours=None, flags=None, endPtsOfContours=None
    )
    drop = None
    simple_glyphs = []
    for i, glyph in enumerate(interpolatable_glyphs):
        if glyph.numberOfContours < 1:
            # ignore composite or empty glyphs
            continue

        for attr in staticAttributes.__dict__:
            expected = getattr(staticAttributes, attr)
            found = getattr(glyph, attr)
            if expected is None:
                setattr(staticAttributes, attr, found)
            elif expected != found:
                raise ValueError(
                    f"Incompatible {attr} for glyph at master index {i}: "
                    f"expected {expected}, found {found}"
                )

        may_drop = set()
        start = 0
        coords = glyph.coordinates
        flags = staticAttributes.flags
        endPtsOfContours = staticAttributes.endPtsOfContours
        for last in endPtsOfContours:
            for i in range(start, last + 1):
                if not (flags[i] & flagOnCurve):
                    continue
                prv = i - 1 if i > start else last
                nxt = i + 1 if i < last else start
                if (flags[prv] & flagOnCurve) or flags[prv] != flags[nxt]:
                    continue
                # we may drop the ith on-curve if halfway between previous/next off-curves
                if not _is_mid_point(coords[prv], coords[i], coords[nxt]):
                    continue

                may_drop.add(i)
            start = last + 1
        # we only want to drop if ALL interpolatable glyphs have the same implied oncurves
        if drop is None:
            drop = may_drop
        else:
            drop.intersection_update(may_drop)

        simple_glyphs.append(glyph)

    if drop:
        # Do the actual dropping
        flags = staticAttributes.flags
        assert flags is not None
        newFlags = array.array(
            "B", (flags[i] for i in range(len(flags)) if i not in drop)
        )

        endPts = staticAttributes.endPtsOfContours
        assert endPts is not None
        newEndPts = []
        i = 0
        delta = 0
        for d in sorted(drop):
            while d > endPts[i]:
                newEndPts.append(endPts[i] - delta)
                i += 1
            delta += 1
        while i < len(endPts):
            newEndPts.append(endPts[i] - delta)
            i += 1

        for glyph in simple_glyphs:
            coords = glyph.coordinates
            glyph.coordinates = GlyphCoordinates(
                coords[i] for i in range(len(coords)) if i not in drop
            )
            glyph.flags = newFlags
            glyph.endPtsOfContours = newEndPts

    return drop if drop is not None else set()

