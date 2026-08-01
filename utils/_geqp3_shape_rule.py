
def _geqp3_shape_rule(a_shape, jpvt_shape, **_):
  m, n = a_shape
  return a_shape, jpvt_shape, (core.min_dim(m, n),)

