
def _bidiagonalize(M, upper=True):
    """
    Returns $B$, the Bidiagonalized form of the input matrix.

    Note: Bidiagonal Computation can hang for symbolic matrices.

    Parameters
    ==========

    upper : bool. Whether to do upper bidiagnalization or lower.
                True for upper and False for lower.

    References
    ==========

    .. [1] Algorithm 5.4.2, Matrix computations by Golub and Van Loan, 4th edition
    .. [2] Complex Matrix Bidiagonalization : https://github.com/vslobody/Householder-Bidiagonalization

    """

    if not isinstance(upper, bool):
        raise ValueError("upper must be a boolean")

    if upper:
        return _eval_bidiag_hholder(M)
    return _eval_bidiag_hholder(M.H).H

