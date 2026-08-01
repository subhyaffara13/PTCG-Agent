
def batch_spec(spec, dim, val):
  too_short = dim - len(spec)
  if too_short > 0:
    spec += (None,) * too_short
  new_partitions = tuple_insert(spec, dim, val)
  return PartitionSpec(*new_partitions)

