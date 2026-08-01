
def ltg_batcher(insert_axis, axis_data, vals_in, dims_in, global_mesh, pspec):
  del insert_axis
  x, = vals_in
  d, = dims_in
  new_parts = None if axis_data.spmd_name is None else axis_data.spmd_name
  new_pspec = list(pspec)
  if d is not None:
    new_pspec.insert(d, new_parts)
  new_pspec = P(*new_pspec)
  y = host_local_array_to_global_array_p.bind(
      x, global_mesh=global_mesh, pspec=new_pspec)
  return y, d

