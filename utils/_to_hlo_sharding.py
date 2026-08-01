
def _to_hlo_sharding(sharding, num_dimensions):
  if not isinstance(sharding, Sharding):
    raise ValueError("Custom Partitioning rules must return Sharding.")
  return sharding._to_xla_hlo_sharding(num_dimensions)

