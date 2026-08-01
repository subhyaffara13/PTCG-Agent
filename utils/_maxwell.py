
def _maxwell(key, shape, dtype, out_sharding) -> Array:
  shape = shape + (3,)
  if out_sharding is not None:
    new_partitions = (*out_sharding.spec, None)
    out_sharding = out_sharding.update(
        spec=out_sharding.spec.update(partitions=new_partitions))
  norm_rvs = normal(key=key, shape=shape, dtype=dtype, out_sharding=out_sharding)
  return jnp_linalg.norm(norm_rvs, axis=-1)

