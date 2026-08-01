
def VarStore_prune_regions(self, *, VarData="VarData", VarRegionList="VarRegionList"):
    """Remove unused VarRegions."""
    #
    # Subset VarRegionList
    #

    # Collect.
    usedRegions = set()
    for data in getattr(self, VarData):
        usedRegions.update(data.VarRegionIndex)
    # Subset.
    regionList = getattr(self, VarRegionList)
    regions = regionList.Region
    newRegions = []
    regionMap = {}
    for i in sorted(usedRegions):
        regionMap[i] = len(newRegions)
        newRegions.append(regions[i])
    regionList.Region = newRegions
    regionList.RegionCount = len(regionList.Region)
    # Map.
    for data in getattr(self, VarData):
        data.VarRegionIndex = [regionMap[i] for i in data.VarRegionIndex]

