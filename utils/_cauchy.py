
def _cauchy(key, shape, dtype) -> Array:
  _check_shape("cauchy", shape)
  u = uniform(key, shape, dtype, minval=dtypes.finfo(dtype).eps, maxval=1.)
  pi = lax._const(u, np.pi)
  return lax.tan(lax.mul(pi, lax.sub(u, lax._const(u, 0.5))))

