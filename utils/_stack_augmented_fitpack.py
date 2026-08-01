
def _stack_augmented_fitpack(A, D, nc, k, p):
    """
    Builds augmented banded matrix.

    Parameters
    ----------
    A : PackedMatrix
        Banded data/design matrix for one axis (from `_dierckx.data_matrix`).
    D : PackedMatrix
        Banded roughness (difference) penalty matrix for the same axis
        (from `disc`).
    nc : int
        Number of top (data) rows from `A` to include.
    k : int
        Spline degree (used only for sizing in the current implementation).
    p : float
        Smoothing parameter. The effective penalization term is scaled as **1/p**:
        larger `p` means *less* smoothing (approaching interpolation).
        If `p == -1`, it signals *p -> inf*, i.e. a pure interpolatory system
        with **no** penalty rows appended.

    Returns
    -------
    AA : ndarray
        Augmented banded matrix with `A` stacked over `(D / p)` when `p != -1`.
    offset : ndarray
        Concatenated band offsets for the augmented matrix.
    nc : int
        Returned unchanged for downstream convenience.
    """
    if p == -1:
        return A.a.copy(), A.offset.copy(), nc

    nz = k + 1
    AA = np.zeros((nc + D.shape[0], k + 2), dtype=float)
    AA[:nc, :nz] = A.a[:nc, :]
    AA[nc:, :] = D.a / p
    offset = np.concatenate((A.offset, D.offset))
    return AA, offset, nc

