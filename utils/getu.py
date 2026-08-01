
def getu(aval):
  if aval.sharding.mesh.are_all_axes_manual:
    return aval.mat.unreduced
  if aval.sharding.mesh.are_all_axes_explicit:
    return aval.sharding.spec.unreduced
  # Revise this after partial manual unreduced is supported
  assert not aval.mat.unreduced
  assert not aval.sharding.spec.unreduced
  return frozenset()

