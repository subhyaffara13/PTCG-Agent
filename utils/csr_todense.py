
def csr_todense(mat: CSR) -> Array:
  """Convert a CSR-format sparse matrix to a dense matrix.

  Args:
    mat : CSR matrix
  Returns:
    mat_dense: dense version of ``mat``
  """
  return _csr_todense(mat.data, mat.indices, mat.indptr, shape=mat.shape)

