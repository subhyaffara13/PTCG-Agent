
def _csr_matvec_impl(data, indices, indptr, v, *, shape, transpose):
  row, col = _csr_to_coo(indices, indptr)
  return _coo_matvec(data, row, col, v, spinfo=COOInfo(shape=shape), transpose=transpose)

