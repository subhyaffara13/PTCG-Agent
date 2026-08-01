
def _coo_matvec(data: Array, row: Array, col: Array, v: Array, *, spinfo: COOInfo, transpose: bool = False) -> Array:
  """Product of COO sparse matrix and a dense vector.

  Args:
    data : array of shape ``(nse,)``.
    row : array of shape ``(nse,)``
    col : array of shape ``(nse,)`` and dtype ``row.dtype``
    v : array of shape ``(shape[0] if transpose else shape[1],)`` and
      dtype ``data.dtype``
    shape : length-2 tuple representing the matrix shape
    transpose : boolean specifying whether to transpose the sparse matrix
      before computing.

  Returns:
    y : array of shape ``(shape[1] if transpose else shape[0],)`` representing
      the matrix vector product.
  """
  return coo_matvec_p.bind(data, row, col, v, spinfo=spinfo, transpose=transpose)

