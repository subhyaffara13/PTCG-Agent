
def _coo_todense(data: Array, row: Array, col: Array, *, spinfo: COOInfo) -> Array:
  """Convert CSR-format sparse matrix to a dense matrix.

  Args:
    data : array of shape ``(nse,)``.
    row : array of shape ``(nse,)``
    col : array of shape ``(nse,)`` and dtype ``row.dtype``
    spinfo : COOInfo object containing matrix metadata

  Returns:
    mat : array with specified shape and dtype matching ``data``
  """
  return coo_todense_p.bind(data, row, col, spinfo=spinfo)

