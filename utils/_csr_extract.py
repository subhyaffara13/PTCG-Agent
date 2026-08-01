
def _csr_extract(indices: Array, indptr: Array, mat: Array) -> Array:
  """Extract values of dense matrix mat at given CSR indices."""
  row, col = _csr_to_coo(indices, indptr)
  return _coo_extract(row, col, mat)

