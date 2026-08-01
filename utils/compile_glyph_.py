
def compileGlyph_(
    dataOffsetSize,
    variations,
    pointCount,
    axisTags,
    sharedCoordIndices,
    *,
    optimizeSize=True,
):
    assert dataOffsetSize in (2, 3)
    tupleVariationCount, tuples, data = tv.compileTupleVariationStore(
        variations, pointCount, axisTags, sharedCoordIndices, optimizeSize=optimizeSize
    )
    if tupleVariationCount == 0:
        return b""

    offsetToData = 2 + dataOffsetSize + len(tuples)

    result = [
        tupleVariationCount.to_bytes(2, "big"),
        offsetToData.to_bytes(dataOffsetSize, "big"),
        tuples,
        data,
    ]
    if (offsetToData + len(data)) % 2 != 0:
        result.append(b"\0")  # padding
    return b"".join(result)

