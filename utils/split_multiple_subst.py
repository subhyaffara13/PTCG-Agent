
def splitMultipleSubst(oldSubTable, newSubTable, overflowRecord):
    ok = 1
    oldMapping = sorted(oldSubTable.mapping.items())
    oldLen = len(oldMapping)

    if overflowRecord.itemName in ["Coverage", "RangeRecord"]:
        # Coverage table is written last. Overflow is to or within the
        # the coverage table. We will just cut the subtable in half.
        newLen = oldLen // 2

    elif overflowRecord.itemName == "Sequence":
        # We just need to back up by two items from the overflowed
        # Sequence index to make sure the offset to the Coverage table
        # doesn't overflow.
        newLen = overflowRecord.itemIndex - 1

    newSubTable.mapping = {}
    for i in range(newLen, oldLen):
        item = oldMapping[i]
        key = item[0]
        newSubTable.mapping[key] = item[1]
        del oldSubTable.mapping[key]

    return ok

