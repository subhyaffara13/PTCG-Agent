
def _csr_matmat_jvp_left(data_dot, data, indices, indptr, B, *, shape, transpose):
  return _csr_matmat(data_dot, indices, indptr, B, shape=shape, transpose=transpose)

