
def estimate_spectral_norm(A, its=20, rng=None):
    """
    Estimate spectral norm of a matrix by the randomized power method.

    ..  This function automatically detects the matrix data type and calls the
        appropriate backend. For details, see :func:`_backend.idd_snorm` and
        :func:`_backend.idz_snorm`.

    Parameters
    ----------
    A : :class:`scipy.sparse.linalg.LinearOperator`
        Matrix given as a :class:`scipy.sparse.linalg.LinearOperator` with the
        `matvec` and `rmatvec` methods (to apply the matrix and its adjoint).
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
        Spectral norm estimate.
    """
    from scipy.sparse.linalg import aslinearoperator
    rng = np.random.default_rng(rng)
    A = aslinearoperator(A)

    if _is_real(A):
        return _backend.idd_snorm(A, its=its, rng=rng)
    else:
        return _backend.idz_snorm(A, its=its, rng=rng)

