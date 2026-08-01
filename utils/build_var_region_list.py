
def buildVarRegionList(supports, axisTags):
    self = ot.VarRegionList()
    self.RegionAxisCount = len(axisTags)
    self.Region = []
    for support in supports:
        self.Region.append(buildVarRegion(support, axisTags))
    self.RegionCount = len(self.Region)
    return self

