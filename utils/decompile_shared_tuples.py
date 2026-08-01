
def decompileSharedTuples(axisTags, sharedTupleCount, data, offset):
    result = []
    for _ in range(sharedTupleCount):
        t, offset = TupleVariation.decompileCoord_(axisTags, data, offset)
        result.append(t)
    return result

