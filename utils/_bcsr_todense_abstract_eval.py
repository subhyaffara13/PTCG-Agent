
def _bcsr_todense_abstract_eval(data, indices, indptr, *, spinfo):
  shape = spinfo.shape
  _validate_bcsr(data, indices, indptr, shape)
  return core.ShapedArray(shape, data.dtype)

