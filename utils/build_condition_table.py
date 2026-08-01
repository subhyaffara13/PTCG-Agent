
def buildConditionTable(axisIndex, filterRangeMinValue, filterRangeMaxValue):
    """Build a ConditionTable."""
    ct = ot.ConditionTable()
    ct.Format = 1
    ct.AxisIndex = axisIndex
    ct.FilterRangeMinValue = filterRangeMinValue
    ct.FilterRangeMaxValue = filterRangeMaxValue
    return ct

