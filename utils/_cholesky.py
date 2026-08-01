
def _cholesky(M, hermitian=True):
    """Returns the Cholesky-type decomposition L of a matrix A
    such that L * L.H == A if hermitian flag is True,
    or L * L.T == A if hermitian is False.

    A must be a Hermitian positive-definite matrix if hermitian is True,
    or a symmetric matrix if it is False.

    Examples
    ========

    >>> from sympy import Matrix
    >>> A = Matrix(((25, 15, -5), (15, 18, 0), (-5, 0, 11)))
    >>> A.cholesky()
    Matrix([
    [ 5, 0, 0],
    [ 3, 3, 0],
    [-1, 1, 3]])
    >>> A.cholesky() * A.cholesky().T
    Matrix([
    [25, 15, -5],
    [15, 18,  0],
    [-5,  0, 11]])

    The matrix can have complex entries:

    >>> from sympy import I
    >>> A = Matrix(((9, 3*I), (-3*I, 5)))
    >>> A.cholesky()
    Matrix([
    [ 3, 0],
    [-I, 2]])
    >>> A.cholesky() * A.cholesky().H
    Matrix([
    [   9, 3*I],
    [-3*I,   5]])

    Non-hermitian Cholesky-type decomposition may be useful when the
    matrix is not positive-definite.

    >>> A = Matrix([[1, 2], [2, 1]])
    >>> L = A.cholesky(hermitian=False)
    >>> L
    Matrix([
    [1,         0],
    [2, sqrt(3)*I]])
    >>> L*L.T == A
    True

    See Also
    ========

    sympy.matrices.dense.DenseMatrix.LDLdecomposition
    sympy.matrices.matrixbase.MatrixBase.LUdecomposition
    QRdecomposition
    """

    from .dense import MutableDenseMatrix

    if not M.is_square:
        raise NonSquareMatrixError("Matrix must be square.")
    if hermitian and not M.is_hermitian:
        raise ValueError("Matrix must be Hermitian.")
    if not hermitian and not M.is_symmetric():
        raise ValueError("Matrix must be symmetric.")

    L   = MutableDenseMatrix.zeros(M.rows, M.rows)

    if hermitian:
        for i in range(M.rows):
            for j in range(i):
                L[i, j] = ((1 / L[j, j])*(M[i, j] -
                    sum(L[i, k]*L[j, k].conjugate() for k in range(j))))

            Lii2 = (M[i, i] -
                sum(L[i, k]*L[i, k].conjugate() for k in range(i)))

            if Lii2.is_positive is False:
                raise NonPositiveDefiniteMatrixError(
                    "Matrix must be positive-definite")

            L[i, i] = sqrt(Lii2)

    else:
        for i in range(M.rows):
            for j in range(i):
                L[i, j] = ((1 / L[j, j])*(M[i, j] -
                    sum(L[i, k]*L[j, k] for k in range(j))))

            L[i, i] = sqrt(M[i, i] -
                sum(L[i, k]**2 for k in range(i)))

    return M._new(L)


def _cholesky(a, lower=False, overwrite_a=False, clean=True,
              check_finite=True):
    """Common code for cholesky() and cho_factor()."""

    # sanity checks
    a1 = _asarray_validated(a, check_finite=check_finite)
    a1 = np.atleast_2d(a1)
    if a1.shape[-1] != a1.shape[-2]:
        raise ValueError(f"Expected a square matrix or batch thereof, got {a1.shape=}")

    _deprecate_dtypes("linalg.cholesky", a1)

    a1, overwrite_a = _normalize_lapack_dtype(a1, overwrite_a)
    a1, overwrite_a = _ensure_aligned_and_native(a1, overwrite_a)
    overwrite_a = (overwrite_a and (a1.ndim == 2)
                   and (a1.flags["F_CONTIGUOUS"] or a1.flags["C_CONTIGUOUS"]))

    # accommodate empty arrays
    if a1.shape[-1] == 0:
        batch_shape = a1.shape[:-2]
        c = np.zeros(batch_shape + (0, 0), dtype=a1.dtype)
        return c

    # Heavy lifting
    c, err_lst = _batched_linalg._cholesky(a1, lower, overwrite_a, clean)

    if err_lst:
        _check_format_errors_warnings("potrf", err_lst)

    return c


def _cholesky(a: ArrayLike, lower: bool) -> Array:
  a, = promote_dtypes_inexact(jnp.asarray(a))
  l = lax_linalg.cholesky(a if lower else jnp.conj(a.mT), symmetrize_input=False)
  return l if lower else jnp.conj(l.mT)

