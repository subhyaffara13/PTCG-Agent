
def _csr_matvec_abstract_eval(data, indices, indptr, v, *, shape, transpose):
  assert len(shape) == 2
  assert v.ndim == data.ndim == indices.ndim == indptr.ndim == 1
  assert data.shape == indices.shape
  assert data.dtype == v.dtype
  assert indices.dtype == indptr.dtype
  assert indptr.shape[0] == shape[0] + 1
  out_shape = shape[1] if transpose else shape[0]
  assert v.shape[0] == (shape[0] if transpose else shape[1])
  return core.ShapedArray((out_shape,), data.dtype)

