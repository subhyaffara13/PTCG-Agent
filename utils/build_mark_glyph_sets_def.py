
def buildMarkGlyphSetsDef(markSets, glyphMap):
    """Builds a mark glyph sets definition table.

    OpenType Layout lookups may choose to use mark filtering sets to consider
    or ignore particular combinations of marks. These sets are specified by
    setting a flag on the lookup, but the mark filtering sets are defined in
    the ``GDEF`` table. This routine builds the subtable containing the mark
    glyph set definitions.

    Example::

        set0 = set("acute", "grave")
        set1 = set("caron", "grave")

        markglyphsets = buildMarkGlyphSetsDef([set0, set1], font.getReverseGlyphMap())

    Args:

        markSets: A list of sets of glyphnames.
        glyphMap: a glyph name to ID map, typically returned from
            ``font.getReverseGlyphMap()``.

    Returns
        An ``otTables.MarkGlyphSetsDef`` object.
    """
    if not markSets:
        return None
    self = ot.MarkGlyphSetsDef()
    self.MarkSetTableFormat = 1
    self.Coverage = [buildCoverage(m, glyphMap) for m in markSets]
    self.MarkSetCount = len(self.Coverage)
    return self

