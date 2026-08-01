
def buildSparseVarRegionAxis(axisIndex, axisSupport):
    self = ot.SparseVarRegionAxis()
    self.AxisIndex = axisIndex
    self.StartCoord, self.PeakCoord, self.EndCoord = [float(v) for v in axisSupport]
    return self

