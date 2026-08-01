
def _physicalize_transform_bwd(f, const_avals, *args):
  return [custom_derivatives.Zero(a) for a in const_avals] + list(
      physicalize(f)(*args)
  )

