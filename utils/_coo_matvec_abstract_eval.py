
def _coo_matvec_abstract_eval(data, row, col, v, *, spinfo, transpose):
  assert data.shape == row.shape == col.shape
  assert data.dtype == v.dtype
  assert row.dtype == col.dtype
  assert len(spinfo.shape) == 2
  assert v.ndim == 1
  assert v.shape[0] == (spinfo.shape[0] if transpose else spinfo.shape[1])
  out_shape = spinfo.shape[1] if transpose else spinfo.shape[0]
  return core.ShapedArray((out_shape,), data.dtype)

