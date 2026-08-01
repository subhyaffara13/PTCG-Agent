
def _ldl_get_d_and_l(ldu, pivs, lower=True, hermitian=True):
    """
    Helper function to extract the diagonal and triangular matrices for
    LDL.T factorization.

    Parameters
    ----------
    ldu : ndarray
        The compact output returned by the LAPACK routing
    pivs : ndarray
        The sanitized array of {0, 1, 2} denoting the sizes of the pivots. For
        every 2 there is a succeeding 0.
    lower : bool, optional
        If set to False, upper triangular part is considered.
    hermitian : bool, optional
        If set to False a symmetric complex array is assumed.

    Returns
    -------
    d : ndarray
        The block diagonal matrix.
    lu : ndarray
        The upper/lower triangular matrix
    """
    is_c = iscomplexobj(ldu)
    d = diag(diag(ldu))
    n = d.shape[0]
    blk_i = 0  # block index

    # row/column offsets for selecting sub-, super-diagonal
    x, y = (1, 0) if lower else (0, 1)

    lu = tril(ldu, -1) if lower else triu(ldu, 1)
    diag_inds = arange(n)
    lu[diag_inds, diag_inds] = 1

    for blk in pivs[pivs != 0]:
        # increment the block index and check for 2s
        # if 2 then copy the off diagonals depending on uplo
        inc = blk_i + blk

        if blk == 2:
            d[blk_i+x, blk_i+y] = ldu[blk_i+x, blk_i+y]
            # If Hermitian matrix is factorized, the cross-offdiagonal element
            # should be conjugated.
            if is_c and hermitian:
                d[blk_i+y, blk_i+x] = ldu[blk_i+x, blk_i+y].conj()
            else:
                d[blk_i+y, blk_i+x] = ldu[blk_i+x, blk_i+y]

            lu[blk_i+x, blk_i+y] = 0.
        blk_i = inc

    return d, lu

