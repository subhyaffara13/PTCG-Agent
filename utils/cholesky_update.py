
def cholesky_update(r_matrix: ArrayLike, w_vector: ArrayLike) -> Array:
  r"""Cholesky rank-1 update.

  Given a Cholesky decomposition :math:`A = R.T \, R` and a vector :math:`w`,
  computes the Cholesky decomposition of :math:`A + w \, w.T` in :math:`O(N^2)`
  time.

  Args:
    r_matrix: An upper-triangular matrix (R) such that :math:`A = R^T \, R`.
    w_vector: A vector :math:`w` for rank-1 update.

  Returns:
    A new upper-triangular matrix :math:`R` defining the Cholesky decomposition
    of :math:`A + w \, w^T`.
  """
  r_matrix, w_vector = core.auto_insert_reshard(r_matrix, w_vector)
  return cholesky_update_p.bind(r_matrix, w_vector)

