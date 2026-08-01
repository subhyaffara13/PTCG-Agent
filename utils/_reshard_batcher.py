
def _reshard_batcher(axis_data, vals_in, dims_in, dst_sharding, concrete_mesh):
  x, = vals_in
  d, = dims_in
  if d is None:
    out = reshard_p.bind(x, dst_sharding=dst_sharding,
                         concrete_mesh=concrete_mesh)
    return out, None
  vmapped_dst_sharding = batching.get_sharding_for_vmap(
      axis_data, dst_sharding, d)
  y = reshard_p.bind(x, dst_sharding=vmapped_dst_sharding,
                     concrete_mesh=concrete_mesh)
  return y, d

