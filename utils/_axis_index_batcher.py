
def _axis_index_batcher(axis_data, vals_in, dims_in, *, axis_name):
  axes = tuple(axis_name) if isinstance(axis_name, (tuple, list)) else (axis_name,)
  if axis_data.name not in axes:
    return axis_index_p.bind(axis_name=axis_name), None
  return lax.iota(np.int32, axis_data.size), 0

