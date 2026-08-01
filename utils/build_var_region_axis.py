
def buildVarRegionAxis(axisSupport):
    self = ot.VarRegionAxis()
    self.StartCoord, self.PeakCoord, self.EndCoord = [float(v) for v in axisSupport]
    return self

