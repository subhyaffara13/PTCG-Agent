
def interp_decomp(A, eps_or_k, rand=True, rng=None):
    """
    Compute ID of a matrix.

    An ID of a matrix `A` is a factorization defined by a rank `k`, a column
    index array `idx`, and interpolation coefficients `proj` such that::

        numpy.dot(A[:,idx[:k]], proj) = A[:,idx[k:]]

    The original matrix can then be reconstructed as::

        numpy.hstack([A[:,idx[:k]],
                                    numpy.dot(A[:,idx[:k]], proj)]
                                )[:,numpy.argsort(idx)]

    or via the routine :func:`reconstruct_matrix_from_id`. This can
    equivalently be written as::

        numpy.dot(A[:,idx[:k]],
                            numpy.hstack([numpy.eye(k), proj])
                          )[:,np.argsort(idx)]

    in terms of the skeleton and interpolation matrices::

        B = A[:,idx[:k]]

    and::

        P = numpy.hstack([numpy.eye(k), proj])[:,np.argsort(idx)]

    respectively. See also :func:`reconstruct_interp_matrix` and
    :func:`reconstruct_skel_matrix`.

    The ID can be computed to any relative precision or rank (depending on the
    value of `eps_or_k`). If a precision is specified (`eps_or_k < 1`), then
    this function has the output signature::

        k, idx, proj = interp_decomp(A, eps_or_k)

    Otherwise, if a rank is specified (`eps_or_k >= 1`), then the output
    signature is::

        idx, proj = interp_decomp(A, eps_or_k)

    ..  This function automatically detects the form of the input parameters
        and passes them to the appropriate backend. For details, see
        :func:`_backend.iddp_id`, :func:`_backend.iddp_aid`,
        :func:`_backend.iddp_rid`, :func:`_backend.iddr_id`,
        :func:`_backend.iddr_aid`, :func:`_backend.iddr_rid`,
        :func:`_backend.idzp_id`, :func:`_backend.idzp_aid`,
        :func:`_backend.idzp_rid`, :func:`_backend.idzr_id`,
        :func:`_backend.idzr_aid`, and :func:`_backend.idzr_rid`.

    Parameters
    ----------
    A : :class:`numpy.ndarray` or :class:`scipy.sparse.linalg.LinearOperator` with `rmatvec`
        Matrix to be factored
    eps_or_k : float or int
        Relative error (if ``eps_or_k < 1``) or rank (if ``eps_or_k >= 1``) of
        approximation.
    rand : bool, optional
        Whether to use random sampling if `A` is of type :class:`numpy.ndarray`
        (randomized algorithms are always used if `A` is of type
        :class:`scipy.sparse.linalg.LinearOperator`).
    rng : `numpy.random.Generator`, optional
        Pseudorandom number generator state. When `rng` is None, a new
        `numpy.random.Generator` is created using entropy from the
        operating system. Types other than `numpy.random.Generator` are
        passed to `numpy.random.default_rng` to instantiate a ``Generator``.
        If `rand` is ``False``, the argument is ignored.

    Returns
    -------
    k : int
        Rank required to achieve specified relative precision if
        ``eps_or_k < 1``.
    idx : :class:`numpy.ndarray`
        Column index array.
    proj : :class:`numpy.ndarray`
        Interpolation coefficients.
    """  # numpy/numpydoc#87  # noqa: E501
    from scipy.sparse.linalg import LinearOperator
    rng = np.random.default_rng(rng)
    real = _is_real(A)

    if isinstance(A, np.ndarray):
        A = _C_contiguous_copy(A)
        if eps_or_k < 1:
            eps = eps_or_k
            if rand:
                if real:
                    k, idx, proj = _backend.iddp_aid(A, eps, rng=rng)
                else:
                    k, idx, proj = _backend.idzp_aid(A, eps, rng=rng)
            else:
                if real:
                    k, idx, proj = _backend.iddp_id(A, eps)
                else:
                    k, idx, proj = _backend.idzp_id(A, eps)
            return k, idx, proj
        else:
            k = int(eps_or_k)
            if rand:
                if real:
                    idx, proj = _backend.iddr_aid(A, k, rng=rng)
                else:
                    idx, proj = _backend.idzr_aid(A, k, rng=rng)
            else:
                if real:
                    idx, proj = _backend.iddr_id(A, k)
                else:
                    idx, proj = _backend.idzr_id(A, k)
            return idx, proj
    elif isinstance(A, LinearOperator):

        if eps_or_k < 1:
            eps = eps_or_k
            if real:
                k, idx, proj = _backend.iddp_rid(A, eps, rng=rng)
            else:
                k, idx, proj = _backend.idzp_rid(A, eps, rng=rng)
            return k, idx, proj
        else:
            k = int(eps_or_k)
            if real:
                idx, proj = _backend.iddr_rid(A, k, rng=rng)
            else:
                idx, proj = _backend.idzr_rid(A, k, rng=rng)
            return idx, proj
    else:
        raise _TYPE_ERROR

