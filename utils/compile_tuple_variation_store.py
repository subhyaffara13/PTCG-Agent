
def compileTupleVariationStore(
    variations,
    pointCount,
    axisTags,
    sharedTupleIndices,
    useSharedPoints=True,
    *,
    optimizeSize=True,
):
    # pointCount is actually unused. Keeping for API compat.
    del pointCount
    newVariations = []
    pointDatas = []
    # Compile all points and figure out sharing if desired
    sharedPoints = None

    # Collect, count, and compile point-sets for all variation sets
    pointSetCount = defaultdict(int)
    for v in variations:
        points = v.getUsedPoints()
        if points is None:  # Empty variations
            continue
        pointSetCount[points] += 1
        newVariations.append(v)
        pointDatas.append(points)
    variations = newVariations
    del newVariations

    if not variations:
        return (0, b"", b"")

    n = len(variations[0].coordinates)
    assert all(
        len(v.coordinates) == n for v in variations
    ), "Variation sets have different sizes"

    compiledPoints = {
        pointSet: TupleVariation.compilePoints(pointSet) for pointSet in pointSetCount
    }

    tupleVariationCount = len(variations)
    tuples = []
    data = []

    if useSharedPoints:
        # Find point-set which saves most bytes.
        def key(pn):
            pointSet = pn[0]
            count = pn[1]
            return len(compiledPoints[pointSet]) * (count - 1)

        sharedPoints = max(pointSetCount.items(), key=key)[0]

        data.append(compiledPoints[sharedPoints])
        tupleVariationCount |= TUPLES_SHARE_POINT_NUMBERS

    # b'' implies "use shared points"
    pointDatas = [
        compiledPoints[points] if points != sharedPoints else b""
        for points in pointDatas
    ]

    for v, p in zip(variations, pointDatas):
        thisTuple, thisData = v.compile(
            axisTags, sharedTupleIndices, pointData=p, optimizeSize=optimizeSize
        )

        tuples.append(thisTuple)
        data.append(thisData)

    tuples = b"".join(tuples)
    data = b"".join(data)
    return tupleVariationCount, tuples, data

