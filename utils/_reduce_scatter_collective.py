
def _reduce_scatter_collective(axis_data, vals_in, dims_in,
                               scatter_dimension, axis_name,
                               axis_index_groups, axis_size, tiled):
  frame_size, frame_name = axis_data.size, axis_data.name
  if not isinstance(axis_name, tuple):
    axis_name = (axis_name,)
  (x,), (d,) = vals_in, dims_in
  if d is None and frame_name not in axis_name:
    out = reduce_scatter_p.bind(
        x, scatter_dimension=scatter_dimension, axis_name=axis_name,
        axis_index_groups=axis_index_groups, axis_size=axis_size,
        tiled=tiled)
    return out, None

  if frame_name not in axis_name:
    return _reduce_scatter_batcher(
        vals_in, dims_in, scatter_dimension=scatter_dimension,
        axis_name=axis_name, axis_index_groups=axis_index_groups,
        axis_size=axis_size, tiled=tiled)
  if axis_index_groups is not None:
    raise NotImplementedError("axis_index_groups not supported in vmap")
  assert axis_size == frame_size, "axis size doesn't match"
  if len(axis_name) > 1:
    raise NotImplementedError("Please open a feature request!")
  assert axis_name == (frame_name,), "batcher called with wrong axis name"
  if d is None:
    y, dy = x * axis_size, scatter_dimension
  else:
    y, dy = lax.reduce(x, 0., lax.add, (d,)), scatter_dimension
  if tiled:
    y = _splitaxis(dy, axis_size, y)
  return y, dy

