
def splitPairPos(oldSubTable, newSubTable, overflowRecord):
    st = oldSubTable
    ok = False
    newSubTable.Format = oldSubTable.Format
    if oldSubTable.Format == 1 and len(oldSubTable.PairSet) > 1:
        for name in "ValueFormat1", "ValueFormat2":
            setattr(newSubTable, name, getattr(oldSubTable, name))

        # Move top half of coverage to new subtable

        newSubTable.Coverage = oldSubTable.Coverage.__class__()

        coverage = oldSubTable.Coverage.glyphs
        records = oldSubTable.PairSet

        oldCount = len(oldSubTable.PairSet) // 2

        oldSubTable.Coverage.glyphs = coverage[:oldCount]
        oldSubTable.PairSet = records[:oldCount]

        newSubTable.Coverage.glyphs = coverage[oldCount:]
        newSubTable.PairSet = records[oldCount:]

        oldSubTable.PairSetCount = len(oldSubTable.PairSet)
        newSubTable.PairSetCount = len(newSubTable.PairSet)

        ok = True

    elif oldSubTable.Format == 2 and len(oldSubTable.Class1Record) > 1:
        if not hasattr(oldSubTable, "Class2Count"):
            oldSubTable.Class2Count = len(oldSubTable.Class1Record[0].Class2Record)
        for name in "Class2Count", "ClassDef2", "ValueFormat1", "ValueFormat2":
            setattr(newSubTable, name, getattr(oldSubTable, name))

        # The two subtables will still have the same ClassDef2 and the table
        # sharing will still cause the sharing to overflow.  As such, disable
        # sharing on the one that is serialized second (that's oldSubTable).
        oldSubTable.DontShare = True

        # Move top half of class numbers to new subtable

        newSubTable.Coverage = oldSubTable.Coverage.__class__()
        newSubTable.ClassDef1 = oldSubTable.ClassDef1.__class__()

        coverage = oldSubTable.Coverage.glyphs
        classDefs = oldSubTable.ClassDef1.classDefs
        records = oldSubTable.Class1Record

        oldCount = len(oldSubTable.Class1Record) // 2
        newGlyphs = set(k for k, v in classDefs.items() if v >= oldCount)

        oldSubTable.Coverage.glyphs = [g for g in coverage if g not in newGlyphs]
        oldSubTable.ClassDef1.classDefs = {
            k: v for k, v in classDefs.items() if v < oldCount
        }
        oldSubTable.Class1Record = records[:oldCount]

        newSubTable.Coverage.glyphs = [g for g in coverage if g in newGlyphs]
        newSubTable.ClassDef1.classDefs = {
            k: (v - oldCount) for k, v in classDefs.items() if v > oldCount
        }
        newSubTable.Class1Record = records[oldCount:]

        oldSubTable.Class1Count = len(oldSubTable.Class1Record)
        newSubTable.Class1Count = len(newSubTable.Class1Record)

        ok = True

    return ok

