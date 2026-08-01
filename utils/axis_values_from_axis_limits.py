
def axisValuesFromAxisLimits(stat, axisLimits):
    def isAxisValueOutsideLimits(axisTag, axisValue):
        if axisTag in axisLimits:
            triple = axisLimits[axisTag]
            if axisValue < triple.minimum or axisValue > triple.maximum:
                return True
        return False

    # only keep AxisValues whose axis is not pinned nor restricted, or is pinned at the
    # exact (nominal) value, or is restricted but the value is within the new range
    designAxes = stat.DesignAxisRecord.Axis
    newAxisValueTables = []
    for axisValueTable in stat.AxisValueArray.AxisValue:
        axisValueFormat = axisValueTable.Format
        if axisValueFormat in (1, 2, 3):
            axisTag = designAxes[axisValueTable.AxisIndex].AxisTag
            if axisValueFormat == 2:
                axisValue = axisValueTable.NominalValue
            else:
                axisValue = axisValueTable.Value
            if isAxisValueOutsideLimits(axisTag, axisValue):
                continue
        elif axisValueFormat == 4:
            # drop 'non-analytic' AxisValue if _any_ AxisValueRecord doesn't match
            # the pinned location or is outside range
            dropAxisValueTable = False
            for rec in axisValueTable.AxisValueRecord:
                axisTag = designAxes[rec.AxisIndex].AxisTag
                axisValue = rec.Value
                if isAxisValueOutsideLimits(axisTag, axisValue):
                    dropAxisValueTable = True
                    break
            if dropAxisValueTable:
                continue
        else:
            log.warning("Unknown AxisValue table format (%s); ignored", axisValueFormat)
        newAxisValueTables.append(axisValueTable)
    return newAxisValueTables

