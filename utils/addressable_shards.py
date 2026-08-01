
def addressable_shards(x: jax.Array | jax.ShapeDtypeStruct) -> list[Index]:
  """Computes list of fragment indices for addressable shards of a JAX array."""
  sharding = getattr(x, 'sharding', None)
  shape = x.shape
  if not sharding:
    return [tuple(slice(0, dim, 1) for dim in shape)]
  return [
      normalize(idx, shape)
      for idx in sharding.addressable_devices_indices_map(shape).values()
  ]

