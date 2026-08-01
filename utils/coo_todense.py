
def coo_todense(mat: COO) -> Array:
  """Convert a COO-format sparse matrix to a dense matrix.

  Args:
    mat : COO matrix
  Returns:
    mat_dense: dense version of ``mat``
  """
  return _coo_todense(mat.data, mat.row, mat.col, spinfo=mat._info)

