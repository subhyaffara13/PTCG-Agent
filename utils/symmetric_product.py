
def symmetric_product(
    a_matrix: ArrayLike,
    c_matrix: ArrayLike,
    *,
    alpha: float = 1.,
    beta: float = 0.,
    symmetrize_output: bool = False
):
  r"""Symmetric product.

  Computes the symmetric product

  .. math::
    \alpha \, A \, A^T + \beta \, C

  where :math:`A` is a rectangular matrix and :math:`C` is a symmetric matrix.

  Args:
    a_matrix: A batch of matrices with shape ``[..., m, n]``.
    c_matrix: A batch of matrices with shape ``[..., m, m]``.
    alpha: A scalar.
    beta: A scalar.
    symmetrize_output: If ``True``, the upper triangle of the output is
      replaced with its transpose.

  Returns:
    A batch of matrices with shape ``[..., m, m]`` where only the lower
    triangle is guaranteed to include the correct values on all platforms. If
    ``symmetrize_output`` is ``True``, the upper triangle is filled with the
    transpose of the lower triangle, and the whole matrix is valid.
  """
  a_matrix, c_matrix = core.auto_insert_reshard(a_matrix, c_matrix)
  result = symmetric_product_p.bind(a_matrix, c_matrix, alpha=alpha, beta=beta)
  if symmetrize_output:
    upper_half = lax.transpose(
        _tril(result, k=-1),
        (*range(result.ndim - 2), result.ndim - 1, result.ndim - 2))
    result = _tril(result, k=0) + upper_half
  return result

