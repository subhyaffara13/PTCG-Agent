
def buildCaretValueForCoord(coord):
    # 500 --> otTables.CaretValue, format 1
    # (500, DeviceTable) --> otTables.CaretValue, format 3
    self = ot.CaretValue()
    if isinstance(coord, tuple):
        self.Format = 3
        self.Coordinate, self.DeviceTable = coord
    else:
        self.Format = 1
        self.Coordinate = coord
    return self

