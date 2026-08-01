
def _all_to_all_batched_collective(axis_data, vals_in, dims_in,
                                   axis_name, split_axis, concat_axis,
                                   axis_index_groups, tiled):
  if axis_index_groups is not None:
    raise NotImplementedError("Please open a feature request!")
  x, = vals_in
  d, = dims_in
  axis_size, frame_name = axis_data.size, axis_data.name
  axes_names = axis_name if isinstance(axis_name, (list, tuple)) else [axis_name]
  if d is None and frame_name not in axes_names:
    out = all_to_all_p.bind(
        x, axis_name=axis_name, split_axis=split_axis, concat_axis=concat_axis,
        axis_index_groups=axis_index_groups, tiled=tiled)
    return out, None
  if frame_name not in axes_names:
    return _all_to_all_batcher(
      vals_in, dims_in, axis_name=axis_name, split_axis=split_axis,
      concat_axis=concat_axis, axis_index_groups=axis_index_groups, tiled=tiled)

  if d is None:
    # TODO(sharadmv,apaszke): Remove this broadcast that comes from
    # all_gather_transpose and instead avoid using all_to_all in
    # all_gather_transpose.
    x = lax.broadcast(x, (axis_size, *x.shape))
    d = 0
  if isinstance(axis_name, (list, tuple)):
    pos = axis_name.index(frame_name)
    major_axes, minor_axes = axis_name[:pos], axis_name[pos + 1:]
  else:
    major_axes, minor_axes = (), ()
  # Optimized case when no splitting is necessary
  if not major_axes and not minor_axes:
    if split_axis == concat_axis:
      axis = split_axis + (d <= split_axis)
      d_pre_split = d
      x = _splitaxis(axis, axis_size, x)
      d += (axis <= d)
      return _foldaxis(axis, moveaxis(x, (d, axis), (axis, d))), d_pre_split
    else:
      x_concat = _foldaxis(concat_axis, _moveaxis(d, concat_axis, x))
      return _splitaxis(split_axis, axis_size, x_concat), split_axis
  # Here we have to handle either the major or the minor dimensions
  # We will be accumulating chunks into the three leading dims: [Major, Current, Minor, ...]
  x, d = lax.expand_dims(_moveaxis(d, 0, x), (0, 2)), 1
  split_axis += 3; concat_axis += 3  # Offset by extra three leading dims

  if major_axes:
    x = all_to_all_p.bind(x, axis_name=major_axes,
                          split_axis=split_axis, concat_axis=0,
                          axis_index_groups=axis_index_groups,
                          tiled=tiled)
  # Split out the local part into axis new_d (NOTE: d is already in axis 1)
  assert d == 1
  x = _splitaxis(split_axis, axis_size, x)
  new_d = split_axis
  concat_axis += (split_axis <= concat_axis)  # Offset the existing axes by the new batch axis
  split_axis += 1
  if minor_axes:
    x = all_to_all_p.bind(x, axis_name=minor_axes,
                          split_axis=split_axis, concat_axis=2,
                          axis_index_groups=axis_index_groups,
                          tiled=tiled)

  # Fold the chunk axes into a single one
  x = _foldaxis(0, _foldaxis(0, x))
  split_axis -= 2; concat_axis -= 2; new_d -= 2
  # Fold gathered axes into concat_axis
  x = _foldaxis(concat_axis - 1, _moveaxis(0, concat_axis - 1, x))
  new_d -= 1  # We've removed 0th dimension, so new_d needs to be adjusted
  return x, new_d

