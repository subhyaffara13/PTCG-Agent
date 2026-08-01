
def _dm_rref_GJ(M):
    """Compute RREF using Gauss-Jordan elimination with division."""
    if M.rep.fmt == 'sparse':
        return _dm_rref_GJ_sparse(M)
    else:
        return _dm_rref_GJ_dense(M)

