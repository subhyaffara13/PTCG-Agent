
def contains_unconstrained(s):
  return (isinstance(s, NamedSharding) and
          PartitionSpec.UNCONSTRAINED in s.spec.partitions)

