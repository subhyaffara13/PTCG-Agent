
def _inv_CH(M, iszerofunc=_iszero):
    """Calculates the inverse using cholesky decomposition.

    See Also
    ========

    inv
    inverse_ADJ
    inverse_GE
    inverse_LU
    inverse_LDL
    """

    _verify_invertible(M, iszerofunc=iszerofunc)

    return M.cholesky_solve(M.eye(M.rows))

