
def GramSchmidt(vlist, orthonormal=False):
    """Apply the Gram-Schmidt process to a set of vectors.

    Parameters
    ==========

    vlist : List of Matrix
        Vectors to be orthogonalized for.

    orthonormal : Bool, optional
        If true, return an orthonormal basis.

    Returns
    =======

    vlist : List of Matrix
        Orthogonalized vectors

    Notes
    =====

    This routine is mostly duplicate from ``Matrix.orthogonalize``,
    except for some difference that this always raises error when
    linearly dependent vectors are found, and the keyword ``normalize``
    has been named as ``orthonormal`` in this function.

    See Also
    ========

    .matrixbase.MatrixBase.orthogonalize

    References
    ==========

    .. [1] https://en.wikipedia.org/wiki/Gram%E2%80%93Schmidt_process
    """
    return MutableDenseMatrix.orthogonalize(
        *vlist, normalize=orthonormal, rankcheck=True
    )

