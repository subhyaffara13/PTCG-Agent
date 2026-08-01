
def estimate_spectral_norm_diff(A, B, its=20, rng=None):
    """
    Estimate spectral norm of the difference of two matrices by the randomized
    power method.

    ..  This function automatically detects the matrix data type and calls the
        appropriate backend. For details, see :func:`_backend.idd_diffsnorm` and
        :func:`_backend.idz_diffsnorm`.

    Parameters
    ----------
    A : :class:`scipy.sparse.linalg.LinearOperator`
        First matrix given as a :class:`scipy.sparse.linalg.LinearOperator` with the
        `matvec` and `rmatvec` methods (to apply the matrix and its adjoint).
    B : :class:`scipy.sparse.linalg.LinearOperator`
        Second matrix given as a :class:`scipy.sparse.linalg.LinearOperator` with
        the `matvec` and `rmatvec` methods (to apply the matrix and its adjoint).
    its : int, optional
        Number of power method iterations.
    rng : `numpy.random.Generator`, optional
        Pseudorandom number generator state. When `rng` is None, a new
        `numpy.random.Generator` is created using entropy from the
        operating system. Types other than `numpy.random.Generator` are
        passed to `numpy.random.default_rng` to instantiate a ``Generator``.
        If `rand` is ``False``, the argument is ignored.

    Returns
    -------
    float
        Spectral norm estimate of matrix difference.
    """
    from scipy.sparse.linalg import aslinearoperator
    rng = np.random.default_rng(rng)
    A = aslinearoperator(A)
    B = aslinearoperator(B)

    if _is_real(A):
        return _backend.idd_diffsnorm(A, B, its=its, rng=rng)
    else:
        return _backend.idz_diffsnorm(A, B, its=its, rng=rng)

