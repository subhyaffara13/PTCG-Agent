
def _add_stat(font):
    # Note: this function only gets called by old code that calls `build()`
    # directly. Newer code that wants to benefit from STAT data from the
    # designspace should call `build_many()`

    if "STAT" in font:
        return

    from ..otlLib.builder import buildStatTable

    fvarTable = font["fvar"]
    axes = [dict(tag=a.axisTag, name=a.axisNameID) for a in fvarTable.axes]
    buildStatTable(font, axes)

