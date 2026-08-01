
def _pinv(M, method='RD'):
    """Calculate the Moore-Penrose pseudoinverse of the matrix.

    The Moore-Penrose pseudoinverse exists and is unique for any matrix.
    If the matrix is invertible, the pseudoinverse is the same as the
    inverse.

    Parameters
    ==========

    method : String, optional
        Specifies the method for computing the pseudoinverse.

        If ``'RD'``, Rank-Decomposition will be used.

        If ``'ED'``, Diagonalization will be used.

    Examples
    ========

    Computing pseudoinverse by rank decomposition :

    >>> from sympy import Matrix
    >>> A = Matrix([[1, 2, 3], [4, 5, 6]])
    >>> A.pinv()
    Matrix([
    [-17/18,  4/9],
    [  -1/9,  1/9],
    [ 13/18, -2/9]])

    Computing pseudoinverse by diagonalization :

    >>> B = A.pinv(method='ED')
    >>> B.simplify()
    >>> B
    Matrix([
    [-17/18,  4/9],
    [  -1/9,  1/9],
    [ 13/18, -2/9]])

    See Also
    ========

    inv
    pinv_solve

    References
    ==========

    .. [1] https://en.wikipedia.org/wiki/Moore-Penrose_pseudoinverse

    """

    # Trivial case: pseudoinverse of all-zero matrix is its transpose.
    if M.is_zero_matrix:
        return M.H

    if method == 'RD':
        return _pinv_rank_decomposition(M)
    elif method == 'ED':
        return _pinv_diagonalization(M)
    else:
        raise ValueError('invalid pinv method %s' % repr(method))


def _pinv(a: ArrayLike, rtol: ArrayLike | None = None, hermitian: bool = False) -> Array:
  # Uses same algorithm as
  # https://github.com/numpy/numpy/blob/v1.17.0/numpy/linalg/linalg.py#L1890-L1979
  a = ensure_arraylike("jnp.linalg.pinv", a)
  arr, = promote_dtypes_inexact(a)
  m, n = arr.shape[-2:]
  if m == 0 or n == 0:
    return array_creation.empty(arr.shape[:-2] + (n, m), arr.dtype)
  arr = ufuncs.conj(arr)
  if rtol is None:
    max_rows_cols = max(arr.shape[-2:])
    rtol = 10. * max_rows_cols * jnp.array(jnp.finfo(arr.dtype).eps)
  rtol = jnp.asarray(rtol)
  u, s, vh = svd(arr, full_matrices=False, hermitian=hermitian)
  # Singular values less than or equal to ``rtol * largest_singular_value``
  # are set to zero.
  rtol = lax.expand_dims(rtol[..., np.newaxis], range(s.ndim - rtol.ndim - 1))
  cutoff = rtol * s[..., 0:1]
  s = jnp.where(s > cutoff, s, np.inf).astype(u.dtype)
  res = tensor_contractions.matmul(vh.mT, ufuncs.divide(u.mT, s[..., np.newaxis]),
                                   precision=lax.Precision.HIGHEST)
  return lax.convert_element_type(res, arr.dtype)

