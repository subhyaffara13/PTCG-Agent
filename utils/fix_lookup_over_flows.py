
def fixLookupOverFlows(ttf, overflowRecord):
    """Either the offset from the LookupList to a lookup overflowed, or
    an offset from a lookup to a subtable overflowed.

    The table layout is::

      GPSO/GUSB
              Script List
              Feature List
              LookUpList
                      Lookup[0] and contents
                              SubTable offset list
                                      SubTable[0] and contents
                                      ...
                                      SubTable[n] and contents
                      ...
                      Lookup[n] and contents
                              SubTable offset list
                                      SubTable[0] and contents
                                      ...
                                      SubTable[n] and contents

    If the offset to a lookup overflowed (SubTableIndex is None)
            we must promote the *previous* lookup to an Extension type.

    If the offset from a lookup to subtable overflowed, then we must promote it
            to an Extension Lookup type.
    """
    ok = 0
    lookupIndex = overflowRecord.LookupListIndex
    if overflowRecord.SubTableIndex is None:
        lookupIndex = lookupIndex - 1
    if lookupIndex < 0:
        return ok
    if overflowRecord.tableType == "GSUB":
        extType = 7
    elif overflowRecord.tableType == "GPOS":
        extType = 9

    lookups = ttf[overflowRecord.tableType].table.LookupList.Lookup
    lookup = lookups[lookupIndex]
    # If the previous lookup is an extType, look further back. Very unlikely, but possible.
    while lookup.SubTable[0].__class__.LookupType == extType:
        lookupIndex = lookupIndex - 1
        if lookupIndex < 0:
            return ok
        lookup = lookups[lookupIndex]

    for lookupIndex in range(lookupIndex, len(lookups)):
        lookup = lookups[lookupIndex]
        if lookup.LookupType != extType:
            lookup.LookupType = extType
            for si, subTable in enumerate(lookup.SubTable):
                extSubTableClass = lookupTypes[overflowRecord.tableType][extType]
                extSubTable = extSubTableClass()
                extSubTable.Format = 1
                extSubTable.ExtSubTable = subTable
                lookup.SubTable[si] = extSubTable
    ok = 1
    return ok

