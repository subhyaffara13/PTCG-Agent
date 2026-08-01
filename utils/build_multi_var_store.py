
def buildMultiVarStore(varRegionList, multiVarDataList):
    self = ot.MultiVarStore()
    self.Format = 1
    self.SparseVarRegionList = varRegionList
    self.MultiVarData = list(multiVarDataList)
    self.MultiVarDataCount = len(self.MultiVarData)
    return self

