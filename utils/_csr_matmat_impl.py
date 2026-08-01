
def _csr_matmat_impl(data, indices, indptr, B, *, shape, transpose):
  row, col = _csr_to_coo(indices, indptr)
  return _coo_matmat(data, row, col, B, spinfo=COOInfo(shape=shape), transpose=transpose)

