
def _spec_to_vma(spec):
  return frozenset(p for s in spec.partitions if s is not None
                   for p in (s if isinstance(s, tuple) else (s,)))

