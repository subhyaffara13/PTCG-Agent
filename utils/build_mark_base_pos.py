
def buildMarkBasePos(marks, bases, glyphMap):
    """Build a list of MarkBasePos (GPOS4) subtables.

    .. deprecated:: 4.58.0
           Use :func:`buildMarkBasePosSubtable` instead.
    """
    return [buildMarkBasePosSubtable(marks, bases, glyphMap)]

