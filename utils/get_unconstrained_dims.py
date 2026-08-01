
def get_unconstrained_dims(sharding: NamedSharding):
  assert sharding.spec is not None
  return frozenset(i for i, axes in enumerate(sharding.spec)
                   if axes is PartitionSpec.UNCONSTRAINED)

