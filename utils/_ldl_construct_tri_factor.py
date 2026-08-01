
def _ldl_construct_tri_factor(lu, swap_vec, pivs, lower=True):
    """
    Helper function to construct explicit outer factors of LDL factorization.

    If lower is True the permuted factors are multiplied as L(1)*L(2)*...*L(k).
    Otherwise, the permuted factors are multiplied as L(k)*...*L(2)*L(1). See
    LAPACK documentation for more details.

    Parameters
    ----------
    lu : ndarray
        The triangular array that is extracted from LAPACK routine call with
        ones on the diagonals.
    swap_vec : ndarray
        The array that defines the row swapping indices. If the kth entry is m
        then rows k,m are swapped. Notice that the mth entry is not necessarily
        k to avoid undoing the swapping.
    pivs : ndarray
        The array that defines the block diagonal structure returned by
        _ldl_sanitize_ipiv().
    lower : bool, optional
        The boolean to switch between lower and upper triangular structure.

    Returns
    -------
    lu : ndarray
        The square outer factor which satisfies the L * D * L.T = A
    perm : ndarray
        The permutation vector that brings the lu to the triangular form

    Notes
    -----
    Note that the original argument "lu" is overwritten.

    """
    n = lu.shape[0]
    perm = arange(n)
    # Setup the reading order of the permutation matrix for upper/lower
    rs, re, ri = (n-1, -1, -1) if lower else (0, n, 1)

    for ind in range(rs, re, ri):
        s_ind = swap_vec[ind]
        if s_ind != ind:
            # Column start and end positions
            col_s = ind if lower else 0
            col_e = n if lower else ind+1

            # If we stumble upon a 2x2 block include both cols in the perm.
            if pivs[ind] == (0 if lower else 2):
                col_s += -1 if lower else 0
                col_e += 0 if lower else 1
            lu[[s_ind, ind], col_s:col_e] = lu[[ind, s_ind], col_s:col_e]
            perm[[s_ind, ind]] = perm[[ind, s_ind]]

    return lu, argsort(perm)

