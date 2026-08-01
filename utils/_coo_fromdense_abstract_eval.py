
def _coo_fromdense_abstract_eval(mat, *, nse, index_dtype):
  data = core.ShapedArray((nse,), mat.dtype)
  row = col = core.ShapedArray((nse,), index_dtype)
  return data, row, col

