
def _csr_matmat_jvp_right(B_dot, data, indices, indptr, B, *, shape, transpose):
  return _csr_matmat(data, indices, indptr, B_dot, shape=shape, transpose=transpose)

