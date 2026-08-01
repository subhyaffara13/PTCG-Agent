
def addEmptyAvar(font):
    """Add an empty `avar` table to the font."""
    font["avar"] = avar = newTable("avar")
    for axis in font["fvar"].axes:
        avar.segments[axis.axisTag] = {}

