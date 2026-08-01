
def _coo_todense_abstract_eval(data, row, col, *, spinfo):
  return core.ShapedArray(spinfo.shape, data.dtype)

