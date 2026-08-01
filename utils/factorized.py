
def factorized(A):
    """
    Return a function for solving a sparse linear system, with A pre-factorized.

    Parameters
    ----------
    A : (N, N) array_like
        Input. A in CSC format is most efficient. A CSR format matrix will
        be converted to CSC before factorization.

    Returns
    -------
    solve : callable
        To solve the linear system of equations given in `A`, the `solve`
        callable should be passed an ndarray of shape (N,).

    Examples
    --------
    >>> import numpy as np
    >>> from scipy.sparse.linalg import factorized
    >>> from scipy.sparse import csc_array
    >>> A = np.array([[ 3. ,  2. , -1. ],
    ...               [ 2. , -2. ,  4. ],
    ...               [-1. ,  0.5, -1. ]])
    >>> solve = factorized(csc_array(A)) # Makes LU decomposition.
    >>> rhs1 = np.array([1, -2, 0])
    >>> solve(rhs1) # Uses the LU factors.
    array([ 1., -2., -2.])

    """
    if is_pydata_spmatrix(A):
        A = A.to_scipy_sparse().tocsc()

    if not hasattr(useUmfpack, 'u'):
        useUmfpack.u = not noScikit

    if useUmfpack.u:
        if noScikit:
            raise RuntimeError('Scikits.umfpack not installed.')

        if not (issparse(A) and A.format == "csc"):
            A = csc_array(A)
            warn('splu converted its input to CSC format',
                 SparseEfficiencyWarning, stacklevel=2)

        A = A._asfptype()  # upcast to a floating point format

        if A.dtype.char not in 'dD':
            raise ValueError("convert matrix data to double, please, using"
                  " .astype(), or set linsolve.useUmfpack.u = False")

        umf_family, A = _get_umf_family(A)
        umf = umfpack.UmfpackContext(umf_family)

        # Make LU decomposition.
        umf.numeric(A)

        def solve(b):
            with np.errstate(divide="ignore", invalid="ignore"):
                # Ignoring warnings with numpy >= 1.23.0, see gh-16523
                result = umf.solve(umfpack.UMFPACK_A, A, b, autoTranspose=True)

            return result

        return solve
    else:
        return splu(A).solve

