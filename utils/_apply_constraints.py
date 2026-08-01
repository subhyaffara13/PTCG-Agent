
def _applyConstraints(blockVectorV, factYBY, blockVectorBY, blockVectorY):
    """Changes blockVectorV in-place."""
    YBV = blockVectorBY.T.conj() @ blockVectorV
    tmp = cho_solve(factYBY, YBV)
    blockVectorV -= blockVectorY @ tmp

