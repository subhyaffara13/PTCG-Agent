
def _prng_key_type_to_physical_spec(
    key_type: api.ShapeDtypeStruct,
) -> api.ShapeDtypeStruct:
  """Converts a PRNG key type to its physical representation."""
  phys = jax.eval_shape(jax.random.key_data, key_type)
  return api.ShapeDtypeStruct(
      shape=phys.shape,
      dtype=phys.dtype,
      sharding=physical_sharding(key_type, key_type.sharding),
  )

