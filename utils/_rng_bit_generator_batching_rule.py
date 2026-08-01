
def _rng_bit_generator_batching_rule(batched_args, batch_dims, *, shape, dtype,
                                     algorithm, out_sharding):
  keys, = batched_args
  bd, = batch_dims
  if bd is None:
    return lax.rng_bit_generator_p.bind(
        keys, shape=shape, dtype=dtype, algorithm=algorithm,
        out_sharding=out_sharding), (None, None)
  keys = batching.moveaxis(keys, bd, 0)
  batch_size = keys.shape[0]
  out_s = (out_sharding.update(spec=(keys.aval.sharding.spec[0], *out_sharding.spec))
           if out_sharding is not None else None)
  key = keys[0]
  new_key, bits = lax.rng_bit_generator_p.bind(
      key, shape=(batch_size, *shape), dtype=dtype, algorithm=algorithm,
      out_sharding=out_s)
  new_keys = slicing.dynamic_update_index_in_dim(keys, new_key, 0, axis=0)
  return (new_keys, bits), (0, 0)

