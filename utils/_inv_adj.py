
def _inv_ADJ(M, iszerofunc=_iszero):
    """Calculates the inverse using the adjugate matrix and a determinant.

    See Also
    ========

    inv
    inverse_GE
    inverse_LU
    inverse_CH
    inverse_LDL
    """

    d = _verify_invertible(M, iszerofunc=iszerofunc)

    return M.adjugate() / d

