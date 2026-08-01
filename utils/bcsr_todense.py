
def bcsr_todense(mat: BCSR) -> Array:
  """Convert batched sparse matrix to a dense matrix.

  Args:
    mat: BCSR matrix.

  Returns:
    The dense version of ``mat``.
  """
  return _bcsr_todense(mat.data, mat.indices, mat.indptr, spinfo=mat._info)

