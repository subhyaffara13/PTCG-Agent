
def splitAlternateSubst(oldSubTable, newSubTable, overflowRecord):
    ok = 1
    if hasattr(oldSubTable, "sortCoverageLast"):
        newSubTable.sortCoverageLast = oldSubTable.sortCoverageLast

    oldAlts = sorted(oldSubTable.alternates.items())
    oldLen = len(oldAlts)

    if overflowRecord.itemName in ["Coverage", "RangeRecord"]:
        # Coverage table is written last. overflow is to or within the
        # the coverage table. We will just cut the subtable in half.
        newLen = oldLen // 2

    elif overflowRecord.itemName == "AlternateSet":
        # We just need to back up by two items
        # from the overflowed AlternateSet index to make sure the offset
        # to the Coverage table doesn't overflow.
        newLen = overflowRecord.itemIndex - 1

    newSubTable.alternates = {}
    for i in range(newLen, oldLen):
        item = oldAlts[i]
        key = item[0]
        newSubTable.alternates[key] = item[1]
        del oldSubTable.alternates[key]

    return ok

