
def _dm_rref_GJ_dense(M):
    """Compute RREF using dense Gauss-Jordan elimination with division."""
    partial_pivot = M.domain.is_RR or M.domain.is_CC
    ddm = M.rep.to_ddm().copy()
    pivots = ddm_irref(ddm, _partial_pivot=partial_pivot)
    M_rref_ddm = DDM(ddm, M.shape, M.domain)
    pivots = tuple(pivots)
    return M.from_rep(M_rref_ddm.to_dfm_or_ddm()), pivots

