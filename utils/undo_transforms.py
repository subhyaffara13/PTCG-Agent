
def undo_transforms(
    aval: jax_core.AbstractValue,
    memory_transforms: Sequence[state_types.Transform],
) -> list[state_types.Transform]:
  """Extract the `Transform`s that reverse the `Transforms`s"""
  if not memory_transforms:
    return []
  transforms: list[state_types.Transform] = []
  avals = [aval]
  for t in memory_transforms[:-1]:
    aval = t.transform_type(aval)
    avals.append(aval)
  for t, a in reversed(list(zip(memory_transforms, avals))):
    transforms.append(t.undo(a))
  return transforms

