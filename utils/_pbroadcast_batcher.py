
def _pbroadcast_batcher(axis_data, vals_in, dims_in, axis_name, source):
  axis_size = axis_data.size
  (v,), (d,) = vals_in, dims_in
  if not isinstance(axis_name, (tuple, list)):
    axis_name = (axis_name,)
  if d is None and axis_data.name not in axis_name:
    return pbroadcast_p.bind(v, axis_name=axis_name, source=source), None
  if axis_data.name not in axis_name:
    return pbroadcast_p.bind(v, axis_name=axis_name, source=source), d
  remaining_axes = tuple(axis for axis in axis_name if axis != axis_data.name)
  if remaining_axes:
    raise NotImplementedError("pbroadcast batcher only supports a single axis")
  assert axis_name[0] == axis_data.name, "pbroadcast batcher called with a wrong axis!"
  assert source >= 0 and source < axis_size, "collective broadcast doesn't fit in the axis size!"
  if axis_size == 1 and remaining_axes:
    return pbroadcast_p.bind(v, source=source, axis_name=remaining_axes), d
  if d is None:
    return v, d
  return v.take([source] * axis_size, d), d

