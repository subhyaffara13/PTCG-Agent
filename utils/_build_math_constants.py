
def _buildMathConstants(constants):
    if not constants:
        return None

    mathConstants = ot.MathConstants()
    for conv in mathConstants.getConverters():
        value = otRound(constants.get(conv.name, 0))
        if conv.tableClass:
            assert issubclass(conv.tableClass, ot.MathValueRecord)
            value = _mathValueRecord(value)
        setattr(mathConstants, conv.name, value)
    return mathConstants

