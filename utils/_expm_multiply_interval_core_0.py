
def _expm_multiply_interval_core_0(A, X, h, mu, q, norm_info, tol, ell, n0):
    """
    A helper function, for the case q <= s.
    """

    # Compute the new values of m_star and s which should be applied
    # over intervals of size t/q
    if norm_info.onenorm() == 0:
        m_star, s = 0, 1
    else:
        norm_info.set_scale(1./q)
        m_star, s = _fragment_3_1(norm_info, n0, tol, ell=ell)
        norm_info.set_scale(1)

    for k in range(q):
        X[k+1] = _expm_multiply_simple_core(A, X[k], h, mu, m_star, s)
    return X, 0

