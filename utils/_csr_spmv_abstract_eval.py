
def _csr_spmv_abstract_eval(data, indices, indptr, x, *, transpose, shape):
  # TODO(tianjianlu) support for batched matvec.
  assert data.ndim == indices.ndim == indptr.ndim == 1
  assert data.shape == indices.shape
  assert indptr.shape[0] == shape[0] + 1
  assert x.ndim == 1

  assert indices.dtype == indptr.dtype
  assert indices.dtype in SUPPORTED_INDEX_DTYPES
  assert data.dtype == x.dtype
  assert x.dtype in SUPPORTED_DATA_DTYPES

  assert len(shape) == 2
  assert x.shape[0] == (shape[0] if transpose else shape[1])

  return core.ShapedArray(
    shape=shape[1:] if transpose else shape[:1],
    dtype=x.dtype)

