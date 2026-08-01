
def buildCaretValueForPoint(point):
    # 4 --> otTables.CaretValue, format 2
    self = ot.CaretValue()
    self.Format = 2
    self.CaretValuePoint = point
    return self

