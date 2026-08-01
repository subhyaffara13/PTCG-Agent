
def buildMarkBasePosSubtable(marks, bases, glyphMap):
    """Build a single MarkBasePos (GPOS4) subtable.

    This builds a mark-to-base lookup subtable containing all of the referenced
    marks and bases.

    Example::

        # a1, a2, a3, a4, a5 = buildAnchor(500, 100), ...

        marks = {"acute": (0, a1), "grave": (0, a1), "cedilla": (1, a2)}
        bases = {"a": {0: a3, 1: a5}, "b": {0: a4, 1: a5}}
        markbaseposes = [buildMarkBasePosSubtable(marks, bases, font.getReverseGlyphMap())]

    Args:
        marks (dict): A dictionary mapping anchors to glyphs; the keys being
            glyph names, and the values being a tuple of mark class number and
            an ``otTables.Anchor`` object representing the mark's attachment
            point. (See :func:`buildMarkArray`.)
        bases (dict): A dictionary mapping anchors to glyphs; the keys being
            glyph names, and the values being dictionaries mapping mark class ID
            to the appropriate ``otTables.Anchor`` object used for attaching marks
            of that class. (See :func:`buildBaseArray`.)
        glyphMap: a glyph name to ID map, typically returned from
            ``font.getReverseGlyphMap()``.

    Returns:
        A ``otTables.MarkBasePos`` object.
    """
    self = ot.MarkBasePos()
    self.Format = 1
    self.MarkCoverage = buildCoverage(marks, glyphMap)
    self.MarkArray = buildMarkArray(marks, glyphMap)
    self.ClassCount = max([mc for mc, _ in marks.values()]) + 1
    self.BaseCoverage = buildCoverage(bases, glyphMap)
    self.BaseArray = buildBaseArray(bases, self.ClassCount, glyphMap)
    return self

