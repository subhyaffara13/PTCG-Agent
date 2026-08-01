
def VarRegion_get_support(self, fvar_axes):
    return {
        fvar_axes[i].axisTag: (reg.StartCoord, reg.PeakCoord, reg.EndCoord)
        for i, reg in enumerate(self.VarRegionAxis)
        if reg.PeakCoord != 0
    }

