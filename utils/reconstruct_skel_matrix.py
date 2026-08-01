
def reconstruct_skel_matrix(A, k, idx):
    """
    Reconstruct skeleton matrix from ID.

    The skeleton matrix can be reconstructed from the original matrix `A` and its
    ID rank and indices `k` and `idx`, respectively, as::

        B = A[:,idx[:k]]

    The original matrix can then be reconstructed via::

        numpy.hstack([B, numpy.dot(B, proj)])[:,numpy.argsort(idx)]

    See also :func:`reconstruct_matrix_from_id` and
    :func:`reconstruct_interp_matrix`.

    ..  This function automatically detects the matrix data type and calls the
        appropriate backend. For details, see :func:`_backend.idd_copycols` and
        :func:`_backend.idz_copycols`.

    Parameters
    ----------
    A : :class:`numpy.ndarray`
        Original matrix.
    k : int
        Rank of ID.
    idx : :class:`numpy.ndarray`
        Column index array.

    Returns
    -------
    :class:`numpy.ndarray`
        Skeleton matrix.
    """
    return A[:, idx[:k]]

