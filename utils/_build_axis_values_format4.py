
def _buildAxisValuesFormat4(locations, axes, ttFont, windowsNames=True, macNames=True):
    axisTagToIndex = {}
    for axisRecordIndex, axisDict in enumerate(axes):
        axisTagToIndex[axisDict["tag"]] = axisRecordIndex

    axisValues = []
    for axisLocationDict in locations:
        axisValRec = ot.AxisValue()
        axisValRec.Format = 4
        axisValRec.ValueNameID = _addName(
            ttFont, axisLocationDict["name"], windows=windowsNames, mac=macNames
        )
        axisValRec.Flags = axisLocationDict.get("flags", 0)
        axisValueRecords = []
        for tag, value in axisLocationDict["location"].items():
            avr = ot.AxisValueRecord()
            avr.AxisIndex = axisTagToIndex[tag]
            avr.Value = value
            axisValueRecords.append(avr)
        axisValueRecords.sort(key=lambda avr: avr.AxisIndex)
        axisValRec.AxisCount = len(axisValueRecords)
        axisValRec.AxisValueRecord = axisValueRecords
        axisValues.append(axisValRec)
    return axisValues

