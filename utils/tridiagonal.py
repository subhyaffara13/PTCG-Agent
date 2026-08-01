
def tridiagonal(
    a: ArrayLike, *, lower: bool=True
) -> tuple[Array, Array, Array, Array]:
  """Reduces a symmetric/Hermitian matrix to tridiagonal form.

  Currently implemented on CPU and GPU only.

  Args:
    a: A floating point or complex matrix or batch of matrices.
    lower: Describes which triangle of the input matrices to use.
      The other triangle is ignored and not accessed.

  Returns:
    A ``(a, d, e, taus)`` tuple. If ``lower=True``, the diagonal and first
    subdiagonal of matrix (or batch of matrices) ``a`` contain the tridiagonal
    representation, and elements below the first subdiagonal contain the
    elementary Householder reflectors, where additionally ``d`` contains the
    diagonal of the matrix and ``e`` contains the first subdiagonal. If
    ``lower=False`` the diagonal and first superdiagonal of the matrix contains
    the tridiagonal representation, and elements above the first superdiagonal
    contain the elementary Householder reflectors, where additionally ``d``
    contains the diagonal of the matrix and ``e`` contains the first
    superdiagonal. ``taus`` contains the scalar factors of the elementary
    Householder reflectors.
  """
  return tridiagonal_p.bind(lax.asarray(a), lower=lower)

