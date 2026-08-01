
def buildCursivePosSubtable(attach, glyphMap):
    """Builds a cursive positioning (GPOS3) subtable.

    Cursive positioning lookups are made up of a coverage table of glyphs,
    and a set of ``EntryExitRecord`` records containing the anchors for
    each glyph. This function builds the cursive positioning subtable.

    Example::

        subtable = buildCursivePosSubtable({
            "AlifIni": (None, buildAnchor(0, 50)),
            "BehMed": (buildAnchor(500,250), buildAnchor(0,50)),
            # ...
        }, font.getReverseGlyphMap())

    Args:
        attach (dict): A mapping between glyph names and a tuple of two
            ``otTables.Anchor`` objects representing entry and exit anchors.
        glyphMap: a glyph name to ID map, typically returned from
            ``font.getReverseGlyphMap()``.

    Returns:
        An ``otTables.CursivePos`` object, or ``None`` if the attachment
        dictionary was empty.
    """
    if not attach:
        return None
    self = ot.CursivePos()
    self.Format = 1
    self.Coverage = buildCoverage(attach.keys(), glyphMap)
    self.EntryExitRecord = []
    for glyph in self.Coverage.glyphs:
        entryAnchor, exitAnchor = attach[glyph]
        rec = ot.EntryExitRecord()
        rec.EntryAnchor = entryAnchor
        rec.ExitAnchor = exitAnchor
        self.EntryExitRecord.append(rec)
    self.EntryExitCount = len(self.EntryExitRecord)
    return self

