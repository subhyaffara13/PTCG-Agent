
def householder_product(a: ArrayLike, taus: ArrayLike) -> Array:
  """Product of elementary Householder reflectors.

  Args:
    a: A matrix with shape ``[..., m, n]``, whose lower triangle contains
      elementary Householder reflectors.
    taus: A vector with shape ``[..., k]``, where ``k < min(m, n)``, containing
      the scalar factors of the elementary Householder reflectors.

  Returns:
    A batch of orthogonal (unitary) matrices with the same shape as ``a``,
    containing the products of the elementary Householder reflectors.
  """
  a, taus = core.auto_insert_reshard(a, taus)
  return householder_product_p.bind(a, taus)

