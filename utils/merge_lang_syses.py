
def mergeLangSyses(lst):
    assert lst

    # TODO Support merging ReqFeatureIndex
    assert all(l.ReqFeatureIndex == 0xFFFF for l in lst)

    self = otTables.LangSys()
    self.LookupOrder = None
    self.ReqFeatureIndex = 0xFFFF
    self.FeatureIndex = mergeFeatureLists(
        [l.FeatureIndex for l in lst if l.FeatureIndex]
    )
    self.FeatureCount = len(self.FeatureIndex)
    return self

