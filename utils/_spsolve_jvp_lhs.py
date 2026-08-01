
def _spsolve_jvp_lhs(data_dot, data, indices, indptr, b, **kwds):
    # d/dM M^-1 b = M^-1 M_dot M^-1 b
    p = spsolve(data, indices, indptr, b, **kwds)
    q = sparse.csr_matvec_p.bind(data_dot, indices, indptr, p,
                                 shape=(indptr.size - 1, len(b)),
                                 transpose=False)
    return -spsolve(data, indices, indptr, q, **kwds)

