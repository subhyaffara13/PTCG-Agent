
def buildSparseVarRegionList(supports, axisTags):
    self = ot.SparseVarRegionList()
    self.RegionAxisCount = len(axisTags)
    self.Region = []
    for support in supports:
        self.Region.append(buildSparseVarRegion(support, axisTags))
    self.RegionCount = len(self.Region)
    return self

