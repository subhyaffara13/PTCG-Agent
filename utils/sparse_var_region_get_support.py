
def SparseVarRegion_get_support(self, fvar_axes):
    return {
        fvar_axes[reg.AxisIndex].axisTag: (reg.StartCoord, reg.PeakCoord, reg.EndCoord)
        for reg in self.SparseVarRegionAxis
    }

