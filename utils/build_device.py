
def buildDevice(deltas):
    """Builds a Device record as part of a ValueRecord or Anchor.

    Device tables specify size-specific adjustments to value records
    and anchors to reflect changes based on the resolution of the output.
    For example, one could specify that an anchor's Y position should be
    increased by 1 pixel when displayed at 8 pixels per em. This routine
    builds device records.

    Args:
        deltas: A dictionary mapping pixels-per-em sizes to the delta
            adjustment in pixels when the font is displayed at that size.

    Returns:
        An ``otTables.Device`` object if any deltas were supplied, or
        ``None`` otherwise.
    """
    if not deltas:
        return None
    self = ot.Device()
    keys = deltas.keys()
    self.StartSize = startSize = min(keys)
    self.EndSize = endSize = max(keys)
    assert 0 <= startSize <= endSize
    self.DeltaValue = deltaValues = [
        deltas.get(size, 0) for size in range(startSize, endSize + 1)
    ]
    maxDelta = max(deltaValues)
    minDelta = min(deltaValues)
    assert minDelta > -129 and maxDelta < 128
    if minDelta > -3 and maxDelta < 2:
        self.DeltaFormat = 1
    elif minDelta > -9 and maxDelta < 8:
        self.DeltaFormat = 2
    else:
        self.DeltaFormat = 3
    return self

