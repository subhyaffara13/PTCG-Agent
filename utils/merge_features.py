
def mergeFeatures(lst):
    assert lst
    self = otTables.Feature()
    self.FeatureParams = None
    self.LookupListIndex = mergeLookupLists(
        [l.LookupListIndex for l in lst if l.LookupListIndex]
    )
    self.LookupCount = len(self.LookupListIndex)
    return self

