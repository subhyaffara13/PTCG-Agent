
def _default_memory_space_rule(prim, *avals, **kwargs):
  if all(a.memory_space == core.MemorySpace.Any for a in avals):
    return core.MemorySpace.Any
  prev_aval = None
  for a in avals:
    if not a.ndim:
      continue
    if prev_aval is not None and prev_aval.memory_space != a.memory_space:
      raise ValueError(
          f'memory_space of all inputs passed to `{prim.name}` must be the'
          f' same. Got one operand with type: {prev_aval.str_short()} and'
          f' another operand with type: {a.str_short()}')
    prev_aval = a
  if prev_aval is None:
    return core.MemorySpace.Device
  return prev_aval.memory_space

