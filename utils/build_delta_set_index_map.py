
def buildDeltaSetIndexMap(varIdxes):
    mapping = list(varIdxes)
    if all(i == v for i, v in enumerate(mapping)):
        return None
    self = ot.DeltaSetIndexMap()
    self.mapping = mapping
    self.Format = 1 if len(mapping) > 0xFFFF else 0
    return self

