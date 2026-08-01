
def estimate_rank(A, eps, rng=None):
    """
    Estimate matrix rank to a specified relative precision using randomized
    methods.

    The matrix `A` can be given as either a :class:`numpy.ndarray` or a
    :class:`scipy.sparse.linalg.LinearOperator`, with different algorithms used
    for each case. If `A` is of type :class:`numpy.ndarray`, then the output
    rank is typically about 8 higher than the actual numerical rank.

    ..  This function automatically detects the form of the input parameters and
        passes them to the appropriate backend. For details,
        see :func:`_backend.idd_estrank`, :func:`_backend.idd_findrank`,
        :func:`_backend.idz_estrank`, and :func:`_backend.idz_findrank`.

    Parameters
    ----------
    A : :class:`numpy.ndarray` or :class:`scipy.sparse.linalg.LinearOperator`
        Matrix whose rank is to be estimated, given as either a
        :class:`numpy.ndarray` or a :class:`scipy.sparse.linalg.LinearOperator`
        with the `rmatvec` method (to apply the matrix adjoint).
    eps : float
        Relative error for numerical rank definition.
    rng : `numpy.random.Generator`, optional
        Pseudorandom number generator state. When `rng` is None, a new
        `numpy.random.Generator` is created using entropy from the
        operating system. Types other than `numpy.random.Generator` are
        passed to `numpy.random.default_rng` to instantiate a ``Generator``.
        If `rand` is ``False``, the argument is ignored.

    Returns
    -------
    int
        Estimated matrix rank.
    """
    from scipy.sparse.linalg import LinearOperator

    rng = np.random.default_rng(rng)
    real = _is_real(A)

    if isinstance(A, np.ndarray):
        A = _C_contiguous_copy(A)
        if real:
            rank, _ = _backend.idd_estrank(A, eps, rng=rng)
        else:
            rank, _ = _backend.idz_estrank(A, eps, rng=rng)
        if rank == 0:
            # special return value for nearly full rank
            rank = min(A.shape)
        return rank
    elif isinstance(A, LinearOperator):
        if real:
            return _backend.idd_findrank(A, eps, rng=rng)[0]
        else:
            return _backend.idz_findrank(A, eps, rng=rng)[0]
    else:
        raise _TYPE_ERROR

