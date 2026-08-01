
def _geqrf_shape_rule(shape):
  m, n = shape
  return shape, (core.min_dim(m, n),)

