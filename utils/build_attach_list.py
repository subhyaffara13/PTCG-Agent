
def buildAttachList(attachPoints, glyphMap):
    """Builds an AttachList subtable.

    A GDEF table may contain an Attachment Point List table (AttachList)
    which stores the contour indices of attachment points for glyphs with
    attachment points. This routine builds AttachList subtables.

    Args:
        attachPoints (dict): A mapping between glyph names and a list of
            contour indices.

    Returns:
        An ``otTables.AttachList`` object if attachment points are supplied,
            or ``None`` otherwise.
    """
    if not attachPoints:
        return None
    self = ot.AttachList()
    self.Coverage = buildCoverage(attachPoints.keys(), glyphMap)
    self.AttachPoint = [buildAttachPoint(attachPoints[g]) for g in self.Coverage.glyphs]
    self.GlyphCount = len(self.AttachPoint)
    return self

