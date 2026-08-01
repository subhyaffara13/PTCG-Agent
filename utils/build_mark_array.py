
def buildMarkArray(marks, glyphMap):
    """Builds a mark array subtable.

    As part of building mark-to-* positioning rules, you will need to define
    a MarkArray subtable, which "defines the class and the anchor point
    for a mark glyph." This function builds the mark array subtable.

    Example::

        mark = {
            "acute": (0, buildAnchor(300,712)),
            # ...
        }
        markarray = buildMarkArray(marks, font.getReverseGlyphMap())

    Args:
        marks (dict): A dictionary mapping anchors to glyphs; the keys being
            glyph names, and the values being a tuple of mark class number and
            an ``otTables.Anchor`` object representing the mark's attachment
            point.
        glyphMap: a glyph name to ID map, typically returned from
            ``font.getReverseGlyphMap()``.

    Returns:
        An ``otTables.MarkArray`` object.
    """
    self = ot.MarkArray()
    self.MarkRecord = []
    for mark in sorted(marks.keys(), key=glyphMap.__getitem__):
        markClass, anchor = marks[mark]
        markrec = buildMarkRecord(markClass, anchor)
        self.MarkRecord.append(markrec)
    self.MarkCount = len(self.MarkRecord)
    return self

