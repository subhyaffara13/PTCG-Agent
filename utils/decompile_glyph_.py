
def decompileGlyph_(dataOffsetSize, pointCount, sharedTuples, axisTags, data):
    assert dataOffsetSize in (2, 3)
    if len(data) < 2 + dataOffsetSize:
        return []

    tupleVariationCount = int.from_bytes(data[:2], "big")
    offsetToData = int.from_bytes(data[2 : 2 + dataOffsetSize], "big")

    dataPos = offsetToData
    return tv.decompileTupleVariationStore(
        "gvar",
        axisTags,
        tupleVariationCount,
        pointCount,
        sharedTuples,
        data,
        2 + dataOffsetSize,
        offsetToData,
    )

