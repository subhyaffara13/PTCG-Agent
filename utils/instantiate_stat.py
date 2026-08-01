
def instantiateSTAT(varfont, axisLimits):
    # 'axisLimits' dict must contain user-space (non-normalized) coordinates

    stat = varfont["STAT"].table
    if not stat.DesignAxisRecord or not (
        stat.AxisValueArray and stat.AxisValueArray.AxisValue
    ):
        return  # STAT table empty, nothing to do

    log.info("Instantiating STAT table")
    newAxisValueTables = axisValuesFromAxisLimits(stat, axisLimits)
    stat.AxisValueCount = len(newAxisValueTables)
    if stat.AxisValueCount:
        stat.AxisValueArray.AxisValue = newAxisValueTables
    else:
        stat.AxisValueArray = None

