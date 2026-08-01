
def _coo_spmm_abstract_eval(data, row, col, x, *, transpose, shape):
  # TODO(jakevdp) support for batched matmat.
  assert data.shape == row.shape == col.shape
  assert row.ndim == 1
  assert x.ndim == 2

  assert row.dtype == col.dtype
  assert row.dtype in SUPPORTED_INDEX_DTYPES

  assert data.dtype == x.dtype
  assert x.dtype in SUPPORTED_DATA_DTYPES

  assert len(shape) == 2
  assert x.shape[0] == (shape[0] if transpose else shape[1])

  return core.ShapedArray(
    shape=(shape[1] if transpose else shape[0], x.shape[1]),
    dtype=x.dtype)

