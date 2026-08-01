
def _evaluateCondition(condition, fvarAxes, location, instancer):
    if condition.Format == 1:
        # ConditionAxisRange
        axisIndex = condition.AxisIndex
        axisTag = fvarAxes[axisIndex].axisTag
        axisValue = location.get(axisTag, 0)
        minValue = condition.FilterRangeMinValue
        maxValue = condition.FilterRangeMaxValue
        return minValue <= axisValue <= maxValue
    elif condition.Format == 2:
        # ConditionValue
        value = condition.DefaultValue
        value += instancer[condition.VarIdx][0]
        return value > 0
    elif condition.Format == 3:
        # ConditionAnd
        for subcondition in condition.ConditionTable:
            if not _evaluateCondition(subcondition, fvarAxes, location, instancer):
                return False
        return True
    elif condition.Format == 4:
        # ConditionOr
        for subcondition in condition.ConditionTable:
            if _evaluateCondition(subcondition, fvarAxes, location, instancer):
                return True
        return False
    elif condition.Format == 5:
        # ConditionNegate
        return not _evaluateCondition(
            condition.conditionTable, fvarAxes, location, instancer
        )
    else:
        return False  # Unkonwn condition format

