
def _bcsr_todense_jvp(data_dot, data, indices, indptr, *, spinfo):
  del data
  return _bcsr_todense(data_dot, indices, indptr, spinfo=spinfo)

