
def _all_gather_batched_collective(prim, axis_data, vals_in, dims_in,
                                   all_gather_dimension, axis_name,
                                   axis_index_groups, axis_size, tiled):
  frame_size, frame_name = axis_data.size, axis_data.name
  if not isinstance(axis_name, tuple):
    axis_name = (axis_name,)
  (x,), (d,) = vals_in, dims_in
  if d is None and axis_data.name not in axis_name:
    kwargs = dict(all_gather_dimension=all_gather_dimension, axis_name=axis_name,
                  axis_size=axis_size, tiled=tiled)
    out = (prim.bind(x, axis_index_groups=axis_index_groups, **kwargs)
           if prim is all_gather_p else prim.bind(x, **kwargs))
    return out, None
  if frame_name not in axis_name:
    return _all_gather_batcher(
        prim, vals_in, dims_in, all_gather_dimension=all_gather_dimension,
        axis_name=axis_name, axis_index_groups=axis_index_groups,
        axis_size=axis_size, tiled=tiled)
  if axis_index_groups is not None:
    raise NotImplementedError("axis_index_groups not supported in vmap")
  assert axis_size == frame_size, "axis size doesn't match"
  if len(axis_name) > 1:
    raise NotImplementedError("Please open a feature request!")
  assert axis_name == (frame_name,), "batcher called with wrong axis name"
  if d is None:
    out_shape = list(np.shape(x))
    out_shape.insert(all_gather_dimension, axis_size)
    broadcast_dims = [i for i in range(len(out_shape)) if i != all_gather_dimension]
    y = lax.broadcast_in_dim(x, out_shape, broadcast_dims)
  else:
    y = _moveaxis(d, all_gather_dimension, x)
  if tiled:
    y = _foldaxis(all_gather_dimension, y)
  return y, None

