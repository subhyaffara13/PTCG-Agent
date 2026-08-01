
def _dm_rref_den_FF_dense(M):
    """Compute RREF using sparse fraction-free Gauss-Jordan elimination."""
    ddm = M.rep.to_ddm().copy()
    den, pivots = ddm_irref_den(ddm, M.domain)
    M_rref_ddm = DDM(ddm, M.shape, M.domain)
    pivots = tuple(pivots)
    return M.from_rep(M_rref_ddm.to_dfm_or_ddm()), den, pivots

