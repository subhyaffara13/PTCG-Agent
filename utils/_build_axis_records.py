
def _buildAxisRecords(axes, ttFont, windowsNames=True, macNames=True):
    axisRecords = []
    axisValues = []
    for axisRecordIndex, axisDict in enumerate(axes):
        axis = ot.AxisRecord()
        axis.AxisTag = axisDict["tag"]
        axis.AxisNameID = _addName(
            ttFont, axisDict["name"], 256, windows=windowsNames, mac=macNames
        )
        axis.AxisOrdering = axisDict.get("ordering", axisRecordIndex)
        axisRecords.append(axis)

        for axisVal in axisDict.get("values", ()):
            axisValRec = ot.AxisValue()
            axisValRec.AxisIndex = axisRecordIndex
            axisValRec.Flags = axisVal.get("flags", 0)
            axisValRec.ValueNameID = _addName(
                ttFont, axisVal["name"], windows=windowsNames, mac=macNames
            )

            if "value" in axisVal:
                axisValRec.Value = axisVal["value"]
                if "linkedValue" in axisVal:
                    axisValRec.Format = 3
                    axisValRec.LinkedValue = axisVal["linkedValue"]
                else:
                    axisValRec.Format = 1
            elif "nominalValue" in axisVal:
                axisValRec.Format = 2
                axisValRec.NominalValue = axisVal["nominalValue"]
                axisValRec.RangeMinValue = axisVal.get(
                    "rangeMinValue", AXIS_VALUE_NEGATIVE_INFINITY
                )
                axisValRec.RangeMaxValue = axisVal.get(
                    "rangeMaxValue", AXIS_VALUE_POSITIVE_INFINITY
                )
            else:
                raise ValueError("Can't determine format for AxisValue")

            axisValues.append(axisValRec)
    return axisRecords, axisValues

