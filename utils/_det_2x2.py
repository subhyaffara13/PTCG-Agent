
def _det_2x2(a: Array) -> Array:
  return (a[..., 0, 0] * a[..., 1, 1] -
           a[..., 0, 1] * a[..., 1, 0])

