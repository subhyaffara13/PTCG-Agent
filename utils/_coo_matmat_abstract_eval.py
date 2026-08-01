
def _coo_matmat_abstract_eval(data, row, col, B, *, spinfo, transpose):
  assert data.shape == row.shape == col.shape
  assert data.dtype == B.dtype
  assert B.ndim == 2
  assert len(spinfo.shape) == 2
  assert B.shape[0] == (spinfo.shape[0] if transpose else spinfo.shape[1])
  out_shape = spinfo.shape[1] if transpose else spinfo.shape[0]
  return core.ShapedArray((out_shape, B.shape[1]), data.dtype)

