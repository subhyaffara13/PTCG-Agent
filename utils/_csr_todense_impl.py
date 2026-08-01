
def _csr_todense_impl(data, indices, indptr, *, shape):
  row, col = _csr_to_coo(indices, indptr)
  return _coo_todense(data, row, col, spinfo=COOInfo(shape=shape))

