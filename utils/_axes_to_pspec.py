
def _axes_to_pspec(axis_name, axis):
  if axis is None:
    return P()
  return P(*[None] * axis + [axis_name])

