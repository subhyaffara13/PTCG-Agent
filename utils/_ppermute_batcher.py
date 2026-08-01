
def _ppermute_batcher(axis_data, vals_in, dims_in, axis_name, perm):
  axis_size, frame_name = axis_data.size, axis_data.name
  (v,), (d,) = vals_in, dims_in
  if not isinstance(axis_name, (tuple, list)):
    axis_name = (axis_name,)
  if d is None and axis_data.name not in axis_name:
    return ppermute_p.bind(v, perm=perm, axis_name=axis_name), None
  if axis_data.name not in axis_name:
    return ppermute_p.bind(v, perm=perm, axis_name=axis_name), d
  remaining_axes = tuple(axis for axis in axis_name if axis != frame_name)
  if remaining_axes:
    return ppermute_p.bind(v, perm=perm, axis_name=remaining_axes), d
  assert axis_name[0] == frame_name, "ppermute batcher called with a wrong axis!"
  assert len(perm) == axis_size, "Permutation doesn't match the axis size!"
  if d is None:
    return v, d
  perm_indices = np.zeros(axis_size, dtype=int)
  for src, dst in perm:
    perm_indices[dst] = src
  return v.take(perm_indices, d), d

