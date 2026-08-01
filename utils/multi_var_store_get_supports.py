
def MultiVarStore_get_supports(self, major, fvarAxes):
    supports = []
    varData = self.MultiVarData[major]
    for regionIdx in varData.VarRegionIndex:
        region = self.SparseVarRegionList.Region[regionIdx]
        support = region.get_support(fvarAxes)
        supports.append(support)
    return supports

