
def buildMarkLigPosSubtable(marks, ligs, glyphMap):
    """Build a single MarkLigPos (GPOS5) subtable.

    This builds a mark-to-base lookup subtable containing all of the referenced
    marks and bases.

    Note that if you are implementing a layout compiler, you may find it more
    flexible to use
    :py:class:`fontTools.otlLib.lookupBuilders.MarkLigPosBuilder` instead.

    Example::

        # a1, a2, a3, a4, a5 = buildAnchor(500, 100), ...
        marks = {
            "acute": (0, a1),
            "grave": (0, a1),
            "cedilla": (1, a2)
        }
        ligs = {
            "f_i": [
                { 0: a3, 1: a5 }, # f
                { 0: a4, 1: a5 }  # i
                ],
        #   "c_t": [{...}, {...}]
        }
        markligpose = buildMarkLigPosSubtable(marks, ligs,
            font.getReverseGlyphMap())

    Args:
        marks (dict): A dictionary mapping anchors to glyphs; the keys being
            glyph names, and the values being a tuple of mark class number and
            an ``otTables.Anchor`` object representing the mark's attachment
            point. (See :func:`buildMarkArray`.)
        ligs (dict): A mapping of ligature names to an array of dictionaries:
            for each component glyph in the ligature, an dictionary mapping
            mark class IDs to anchors. (See :func:`buildLigatureArray`.)
        glyphMap: a glyph name to ID map, typically returned from
            ``font.getReverseGlyphMap()``.

    Returns:
        A ``otTables.MarkLigPos`` object.
    """
    self = ot.MarkLigPos()
    self.Format = 1
    self.MarkCoverage = buildCoverage(marks, glyphMap)
    self.MarkArray = buildMarkArray(marks, glyphMap)
    self.ClassCount = max([mc for mc, _ in marks.values()]) + 1
    self.LigatureCoverage = buildCoverage(ligs, glyphMap)
    self.LigatureArray = buildLigatureArray(ligs, self.ClassCount, glyphMap)
    return self

