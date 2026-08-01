
def buildBaseArray(bases, numMarkClasses, glyphMap):
    """Builds a base array record.

    As part of building mark-to-base positioning rules, you will need to define
    a ``BaseArray`` record, which "defines for each base glyph an array of
    anchors, one for each mark class." This function builds the base array
    subtable.

    Example::

        bases = {"a": {0: a3, 1: a5}, "b": {0: a4, 1: a5}}
        basearray = buildBaseArray(bases, 2, font.getReverseGlyphMap())

    Args:
        bases (dict): A dictionary mapping anchors to glyphs; the keys being
            glyph names, and the values being dictionaries mapping mark class ID
            to the appropriate ``otTables.Anchor`` object used for attaching marks
            of that class.
        numMarkClasses (int): The total number of mark classes for which anchors
            are defined.
        glyphMap: a glyph name to ID map, typically returned from
            ``font.getReverseGlyphMap()``.

    Returns:
        An ``otTables.BaseArray`` object.
    """
    self = ot.BaseArray()
    self.BaseRecord = []
    for base in sorted(bases, key=glyphMap.__getitem__):
        b = bases[base]
        anchors = [b.get(markClass) for markClass in range(numMarkClasses)]
        self.BaseRecord.append(buildBaseRecord(anchors))
    self.BaseCount = len(self.BaseRecord)
    return self

