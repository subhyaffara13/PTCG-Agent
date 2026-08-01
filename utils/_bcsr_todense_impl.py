
def _bcsr_todense_impl(data, indices, indptr, *, spinfo):
  shape = spinfo.shape
  bcoo_indices = _bcsr_to_bcoo(indices, indptr, shape=shape)
  return (bcoo.BCOO((data, bcoo_indices), shape=shape)).todense()

