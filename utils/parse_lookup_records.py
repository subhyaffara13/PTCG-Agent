
def parseLookupRecords(items, klassName, lookupMap=None):
    klass = getattr(ot, klassName)
    lst = []
    for item in items:
        rec = klass()
        item = stripSplitComma(item)
        assert len(item) == 2, item
        idx = int(item[0])
        assert idx > 0, idx
        rec.SequenceIndex = idx - 1
        setReference(mapLookup, lookupMap, item[1], setattr, rec, "LookupListIndex")
        lst.append(rec)
    return lst

