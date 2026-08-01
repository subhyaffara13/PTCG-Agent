
def buildMarkLigPos(marks, ligs, glyphMap):
    """Build a list of MarkLigPos (GPOS5) subtables.

    .. deprecated:: 4.58.0
       Use :func:`buildMarkLigPosSubtable` instead.
    """
    return [buildMarkLigPosSubtable(marks, ligs, glyphMap)]

