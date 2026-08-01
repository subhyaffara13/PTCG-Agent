
def all_unconstrained(s, aval):
  if isinstance(s, NamedSharding):
    if aval.ndim == 0:
      return False
    if aval.ndim != len(s.spec):
      return False
    return all(p is PartitionSpec.UNCONSTRAINED for p in s.spec.partitions)
  return False

