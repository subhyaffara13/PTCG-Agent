
def buildSingleSubstSubtable(mapping):
    """Builds a single substitution (GSUB1) subtable.

    Note that if you are implementing a layout compiler, you may find it more
    flexible to use
    :py:class:`fontTools.otlLib.lookupBuilders.SingleSubstBuilder` instead.

    Args:
        mapping: A dictionary mapping input glyph names to output glyph names.

    Returns:
        An ``otTables.SingleSubst`` object, or ``None`` if the mapping dictionary
        is empty.
    """
    if not mapping:
        return None
    self = ot.SingleSubst()
    self.mapping = dict(mapping)
    return self

