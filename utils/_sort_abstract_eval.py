
def _sort_abstract_eval(*avals, dimension, is_stable, num_keys):
  avals = tuple(avals)
  if any(arg.shape != avals[0].shape for arg in avals[1:]):
    shapes = " ".join(str(a.shape) for a in avals)
    raise TypeError(f"Arguments to sort must have equal shapes, got: {shapes}")
  non_empty_s = [
      a.sharding for a in avals
      if not a.sharding.mesh.empty and a.sharding.mesh._any_axis_explicit]
  for s in non_empty_s:
    if s.spec[dimension] is not None:
      raise core.ShardingTypeError(
          "Arguments to sort must be unsharded over the sorting dimension. "
          f"Got arg sharding={s} and sorting dimension={dimension}")
    if s != non_empty_s[0]:
      shardings = " ".join(str(s) for s in non_empty_s)
      raise core.ShardingTypeError(
          f'Arguments to sort must have equal shardings, got: {shardings}')
  return avals

