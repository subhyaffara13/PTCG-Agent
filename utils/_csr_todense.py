
def _csr_todense(data: Array, indices: Array, indptr: Array, *, shape: Shape) -> Array:
  """Convert CSR-format sparse matrix to a dense matrix.

  Args:
    data : array of shape ``(nse,)``.
    indices : array of shape ``(nse,)``
    indptr : array of shape ``(shape[0] + 1,)`` and dtype ``indices.dtype``
    shape : length-2 tuple representing the matrix shape

  Returns:
    mat : array with specified shape and dtype matching ``data``
  """
  return csr_todense_p.bind(data, indices, indptr, shape=shape)

