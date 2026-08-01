
def _getValueFormat(f, values, i):
    # Helper for buildPairPos{Glyphs|Classes}Subtable.
    if f is not None:
        return f
    mask = 0
    for value in values:
        if value is not None and value[i] is not None:
            mask |= value[i].getFormat()
    return mask

