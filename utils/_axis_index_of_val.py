
def _axis_index_of_val(x, val, axis_name):
  idx = axis_index(axis_name)
  mask = (val == x)
  validx = lax.select(mask,
                      lax.full(mask.shape, idx),
                      lax.full(mask.shape, dtypes.iinfo(idx.dtype).max, idx.dtype))
  return pmin(validx, axis_name)

