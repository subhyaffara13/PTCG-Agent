
def buildMultiVarData(varRegionIndices, items):
    self = ot.MultiVarData()
    self.Format = 1
    self.VarRegionIndex = list(varRegionIndices)
    regionCount = self.VarRegionCount = len(self.VarRegionIndex)
    records = self.Item = []
    if items:
        for item in items:
            assert len(item) == regionCount
            records.append(list(item))
    self.ItemCount = len(self.Item)
    return self

