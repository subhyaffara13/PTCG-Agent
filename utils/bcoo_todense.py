
def bcoo_todense(mat: BCOO) -> Array:
  """Convert batched sparse matrix to a dense matrix.

  Args:
    mat: BCOO matrix.

  Returns:
    mat_dense: dense version of ``mat``.
  """
  return _bcoo_todense(mat.data, mat.indices, spinfo=mat._info)

