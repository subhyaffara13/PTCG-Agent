
def _csr_matvec_jvp_vec(v_dot, data, indices, indptr, v, *, shape, transpose):
  return _csr_matvec(data, indices, indptr, v_dot, shape=shape, transpose=transpose)

