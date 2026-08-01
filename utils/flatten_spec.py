
def flatten_spec(spec):
  out = []
  for s in (spec.partitions if isinstance(spec, PartitionSpec) else spec):
    if isinstance(s, tuple):
      out.extend(s)
    else:
      out.append(s)
  return out

