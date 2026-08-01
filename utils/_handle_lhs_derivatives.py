
def _handle_lhs_derivatives(t, k, xval, ab, kl, ku, deriv_ords, offset=0):
    """ Fill in the entries of the colocation matrix corresponding to known
    derivatives at `xval`.

    The colocation matrix is in the banded storage, as prepared by _coloc.
    No error checking.

    Parameters
    ----------
    t : ndarray, shape (nt + k + 1,)
        knots
    k : int
        B-spline order
    xval : float
        The value at which to evaluate the derivatives at.
    ab : ndarray, shape(2*kl + ku + 1, nt), Fortran order
        B-spline colocation matrix.
        This argument is modified *in-place*.
    kl : int
        Number of lower diagonals of ab.
    ku : int
        Number of upper diagonals of ab.
    deriv_ords : 1D ndarray
        Orders of derivatives known at xval
    offset : int, optional
        Skip this many rows of the matrix ab.

    """
    # find where `xval` is in the knot vector, `t`
    left = _dierckx.find_interval(t, k, float(xval), k, False)

    # compute and fill in the derivatives @ xval
    for row in range(deriv_ords.shape[0]):
        nu = deriv_ords[row]
        wrk = _dierckx.evaluate_all_bspl(t, k, xval, left, nu)

        # if A were a full matrix, it would be just
        # ``A[row + offset, left-k:left+1] = bb``.
        for a in range(k+1):
            clmn = left - k + a
            ab[kl + ku + offset + row - clmn, clmn] = wrk[a]

