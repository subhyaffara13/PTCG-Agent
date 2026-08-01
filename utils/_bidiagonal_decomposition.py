
def _bidiagonal_decomposition(M, upper=True):
    """
    Returns $(U,B,V.H)$ for

    $$A = UBV^{H}$$

    where $A$ is the input matrix, and $B$ is its Bidiagonalized form

    Note: Bidiagonal Computation can hang for symbolic matrices.

    Parameters
    ==========

    upper : bool. Whether to do upper bidiagnalization or lower.
                True for upper and False for lower.

    References
    ==========

    .. [1] Algorithm 5.4.2, Matrix computations by Golub and Van Loan, 4th edition
    .. [2] Complex Matrix Bidiagonalization, https://github.com/vslobody/Householder-Bidiagonalization

    """

    if not isinstance(upper, bool):
        raise ValueError("upper must be a boolean")

    if upper:
        return _bidiagonal_decmp_hholder(M)

    X = _bidiagonal_decmp_hholder(M.H)
    return X[2].H, X[1].H, X[0].H

