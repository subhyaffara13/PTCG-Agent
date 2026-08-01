
def _spsolve_jvp_rhs(b_dot, data, indices, indptr, b, **kwds):
    # d/db M^-1 b = M^-1 b_dot
    return spsolve(data, indices, indptr, b_dot, **kwds)

