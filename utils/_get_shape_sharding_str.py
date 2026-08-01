
def _get_shape_sharding_str(shape, spec):
  out = []
  for s1, s2 in zip(shape, spec.partitions):
    if s2 is None:
      out.append(f"{s1}")
    elif isinstance(s2, tuple):
      ss = ','.join(s for s in s2)
      out.append(f"{s1}@({ss})")
    else:
      out.append(f"{s1}@{s2}")
  return ','.join(out)

