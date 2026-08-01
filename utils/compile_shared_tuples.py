
def compileSharedTuples(
    axisTags, variations, MAX_NUM_SHARED_COORDS=TUPLE_INDEX_MASK + 1
):
    coordCount = Counter()
    for var in variations:
        coord = var.compileCoord(axisTags)
        coordCount[coord] += 1
    # In python < 3.7, most_common() ordering is non-deterministic
    # so apply a sort to make sure the ordering is consistent.
    sharedCoords = sorted(
        coordCount.most_common(MAX_NUM_SHARED_COORDS),
        key=lambda item: (-item[1], item[0]),
    )
    return [c[0] for c in sharedCoords if c[1] > 1]

