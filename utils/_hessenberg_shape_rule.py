
def _hessenberg_shape_rule(shape, **_):
  if shape[0] != shape[-1]:
    raise ValueError(
        "Argument to Hessenberg reduction must have shape [..., n, n], "
        f"got shape {shape}"
    )
  return shape, shape[:-2] + (shape[-1] - 1,)

