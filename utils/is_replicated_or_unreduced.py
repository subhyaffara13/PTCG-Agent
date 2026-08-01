
def is_replicated_or_unreduced(sharding: NamedSharding) -> bool:
  if sharding.spec.partitions:
    return False
  if sharding.spec.reduced:
    return False
  if (sharding.spec.unreduced and
      sharding.spec.unreduced != set(sharding.mesh.axis_names)):
    return False
  return True

