
def MultiVarStore_prune_regions(self):
    return ot.VarStore.prune_regions(
        self, VarData="MultiVarData", VarRegionList="SparseVarRegionList"
    )

