
def buildSparseVarRegion(support, axisTags):
    assert all(tag in axisTags for tag in support.keys()), (
        "Unknown axis tag found.",
        support,
        axisTags,
    )
    self = ot.SparseVarRegion()
    self.SparseVarRegionAxis = []
    for i, tag in enumerate(axisTags):
        if tag not in support:
            continue
        self.SparseVarRegionAxis.append(
            buildSparseVarRegionAxis(i, support.get(tag, (0, 0, 0)))
        )
    self.SparseRegionCount = len(self.SparseVarRegionAxis)
    return self

