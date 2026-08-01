
def map_sharding(f, sharding):
  if isinstance(sharding, PartitionSpec) or isinstance(sharding, tuple):
    return PartitionSpec(*map(f, sharding))
  elif isinstance(sharding, NamedSharding):
    return NamedSharding(sharding.mesh, map_sharding(f, sharding.spec)) # type: ignore
  elif isinstance(sharding, Format):
    return Format(sharding.layout, map_sharding(f, sharding.sharding))  # type: ignore

