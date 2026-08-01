
def _to_jax_sharded_shape(s, sharding):
  return api.ShapeDtypeStruct(
      s.dimensions(), s.numpy_dtype(), sharding=sharding
  )

