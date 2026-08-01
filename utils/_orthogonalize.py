
def _orthogonalize(matrices, epsilon=0):
    """
    Decide between Gram-Schmidt or QR factorization to orthogonalize a batch of matrices.

    QR factorization doesn't work with half-precision, but it is usually faster with a rank > 2.
    """
    if not (len(matrices.shape) == 3 and matrices.shape[2] <= matrices.shape[1]):
        raise AssertionError

    num_matrices = matrices.shape[0]
    rank = matrices.shape[2]
    dtype = matrices.dtype
    if rank <= 2 or dtype in [torch.float16, torch.bfloat16]:
        _orthogonalize_gram_schmidt(matrices, epsilon=epsilon)
    else:
        torch.linalg.qr(
            matrices,
            out=(
                matrices,
                torch.empty(
                    num_matrices, rank, rank, device=matrices.device, dtype=dtype
                ),
            ),
        )


def _orthogonalize(cls, *vecs, normalize=False, rankcheck=False):
    """Apply the Gram-Schmidt orthogonalization procedure
    to vectors supplied in ``vecs``.

    Parameters
    ==========

    vecs
        vectors to be made orthogonal

    normalize : bool
        If ``True``, return an orthonormal basis.

    rankcheck : bool
        If ``True``, the computation does not stop when encountering
        linearly dependent vectors.

        If ``False``, it will raise ``ValueError`` when any zero
        or linearly dependent vectors are found.

    Returns
    =======

    list
        List of orthogonal (or orthonormal) basis vectors.

    Examples
    ========

    >>> from sympy import I, Matrix
    >>> v = [Matrix([1, I]), Matrix([1, -I])]
    >>> Matrix.orthogonalize(*v)
    [Matrix([
    [1],
    [I]]), Matrix([
    [ 1],
    [-I]])]

    See Also
    ========

    MatrixBase.QRdecomposition

    References
    ==========

    .. [1] https://en.wikipedia.org/wiki/Gram%E2%80%93Schmidt_process
    """
    from .decompositions import _QRdecomposition_optional

    if not vecs:
        return []

    all_row_vecs = (vecs[0].rows == 1)

    vecs = [x.vec() for x in vecs]
    M = cls.hstack(*vecs)
    Q, R = _QRdecomposition_optional(M, normalize=normalize)

    if rankcheck and Q.cols < len(vecs):
        raise ValueError("GramSchmidt: vector set not linearly independent")

    ret = []
    for i in range(Q.cols):
        if all_row_vecs:
            col = cls(Q[:, i].T)
        else:
            col = cls(Q[:, i])
        ret.append(col)
    return ret

