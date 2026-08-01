
def splitMarkBasePos(oldSubTable, newSubTable, overflowRecord):
    # split half of the mark classes to the new subtable
    classCount = oldSubTable.ClassCount
    if classCount < 2:
        # oh well, not much left to split...
        return False

    oldClassCount = classCount // 2
    newClassCount = classCount - oldClassCount

    oldMarkCoverage, oldMarkRecords = [], []
    newMarkCoverage, newMarkRecords = [], []
    for glyphName, markRecord in zip(
        oldSubTable.MarkCoverage.glyphs, oldSubTable.MarkArray.MarkRecord
    ):
        if markRecord.Class < oldClassCount:
            oldMarkCoverage.append(glyphName)
            oldMarkRecords.append(markRecord)
        else:
            markRecord.Class -= oldClassCount
            newMarkCoverage.append(glyphName)
            newMarkRecords.append(markRecord)

    oldBaseRecords, newBaseRecords = [], []
    for rec in oldSubTable.BaseArray.BaseRecord:
        oldBaseRecord, newBaseRecord = rec.__class__(), rec.__class__()
        oldBaseRecord.BaseAnchor = rec.BaseAnchor[:oldClassCount]
        newBaseRecord.BaseAnchor = rec.BaseAnchor[oldClassCount:]
        oldBaseRecords.append(oldBaseRecord)
        newBaseRecords.append(newBaseRecord)

    newSubTable.Format = oldSubTable.Format

    oldSubTable.MarkCoverage.glyphs = oldMarkCoverage
    newSubTable.MarkCoverage = oldSubTable.MarkCoverage.__class__()
    newSubTable.MarkCoverage.glyphs = newMarkCoverage

    # share the same BaseCoverage in both halves
    newSubTable.BaseCoverage = oldSubTable.BaseCoverage

    oldSubTable.ClassCount = oldClassCount
    newSubTable.ClassCount = newClassCount

    oldSubTable.MarkArray.MarkRecord = oldMarkRecords
    newSubTable.MarkArray = oldSubTable.MarkArray.__class__()
    newSubTable.MarkArray.MarkRecord = newMarkRecords

    oldSubTable.MarkArray.MarkCount = len(oldMarkRecords)
    newSubTable.MarkArray.MarkCount = len(newMarkRecords)

    oldSubTable.BaseArray.BaseRecord = oldBaseRecords
    newSubTable.BaseArray = oldSubTable.BaseArray.__class__()
    newSubTable.BaseArray.BaseRecord = newBaseRecords

    oldSubTable.BaseArray.BaseCount = len(oldBaseRecords)
    newSubTable.BaseArray.BaseCount = len(newBaseRecords)

    return True

