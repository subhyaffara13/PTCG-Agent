
def _csr_todense_jvp(data_dot, data, indices, indptr, *, shape):
  return _csr_todense(data_dot, indices, indptr, shape=shape)

