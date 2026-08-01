
def getr(x, y, N):
    fraction = continued_fraction(x, y)
    # Now convert into r
    total = ratioize(fraction, N)
    return total


def getr(aval):
  if aval.sharding.mesh.are_all_axes_manual:
    return aval.mat.reduced
  if aval.sharding.mesh.are_all_axes_explicit:
    return aval.sharding.spec.reduced
  # Revise this after partial manual reduced is supported
  assert not aval.mat.reduced
  assert not aval.sharding.spec.reduced
  return frozenset()

