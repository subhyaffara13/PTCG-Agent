
def _csr_matvec_jvp_mat(data_dot, data, indices, indptr, v, *, shape, transpose):
  return _csr_matvec(data_dot, indices, indptr, v, shape=shape, transpose=transpose)

