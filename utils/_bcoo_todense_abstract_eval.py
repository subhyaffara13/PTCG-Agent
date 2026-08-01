
def _bcoo_todense_abstract_eval(data, indices, *, spinfo):
  shape = spinfo.shape
  _validate_bcoo(data, indices, shape)
  return core.ShapedArray(shape, data.dtype)

