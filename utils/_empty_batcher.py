
def _empty_batcher(axis_data, vals_in, dims_in, *, shape, dtype, out_sharding):
  batched_shape = tuple_insert(shape, 0, axis_data.size)
  batched_out_sharding = (
      None if out_sharding is None else
      batching.get_sharding_for_vmap(axis_data, out_sharding, 0))
  y = empty_p.bind(shape=batched_shape, dtype=dtype,
                   out_sharding=batched_out_sharding)
  return y, 0

