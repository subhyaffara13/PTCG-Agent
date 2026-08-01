
def _csr_fromdense_abstract_eval(mat, *, nse, index_dtype):
  data = core.ShapedArray((nse,), mat.dtype)
  indices = core.ShapedArray((nse,), index_dtype)
  indptr = core.ShapedArray((mat.shape[0] + 1,), index_dtype)
  return data, indices, indptr

