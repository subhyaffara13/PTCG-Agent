
def buildLigatureArray(ligs, numMarkClasses, glyphMap):
    """Builds a LigatureArray subtable.

    As part of building a mark-to-ligature lookup, you will need to define
    the set of anchors (for each mark class) on each component of the ligature
    where marks can be attached. For example, for an Arabic divine name ligature
    (lam lam heh), you may want to specify mark attachment positioning for
    superior marks (fatha, etc.) and inferior marks (kasra, etc.) on each glyph
    of the ligature. This routine builds the ligature array record.

    Example::

        buildLigatureArray({
            "lam-lam-heh": [
                { 0: superiorAnchor1, 1: inferiorAnchor1 }, # attach points for lam1
                { 0: superiorAnchor2, 1: inferiorAnchor2 }, # attach points for lam2
                { 0: superiorAnchor3, 1: inferiorAnchor3 }, # attach points for heh
            ]
        }, 2, font.getReverseGlyphMap())

    Args:
        ligs (dict): A mapping of ligature names to an array of dictionaries:
            for each component glyph in the ligature, an dictionary mapping
            mark class IDs to anchors.
        numMarkClasses (int): The number of mark classes.
        glyphMap: a glyph name to ID map, typically returned from
            ``font.getReverseGlyphMap()``.

    Returns:
        An ``otTables.LigatureArray`` object if deltas were supplied.
    """
    self = ot.LigatureArray()
    self.LigatureAttach = []
    for lig in sorted(ligs, key=glyphMap.__getitem__):
        anchors = []
        for component in ligs[lig]:
            anchors.append([component.get(mc) for mc in range(numMarkClasses)])
        self.LigatureAttach.append(buildLigatureAttach(anchors))
    self.LigatureCount = len(self.LigatureAttach)
    return self

