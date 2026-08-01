
def _csr_matmat_abstract_eval(data, indices, indptr, B, *, shape, transpose):
  assert len(shape) == 2
  assert data.ndim == indices.ndim == indptr.ndim == 1
  assert B.ndim == 2
  assert data.shape == indices.shape
  assert data.dtype == B.dtype
  assert indices.dtype == indptr.dtype
  assert indptr.shape[0] == shape[0] + 1
  out_shape = shape[1] if transpose else shape[0]
  assert B.shape[0] == (shape[0] if transpose else shape[1])
  return core.ShapedArray((out_shape, B.shape[1]), data.dtype)

