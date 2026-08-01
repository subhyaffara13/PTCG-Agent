
def _laplace(m, d):
    return lambda v: v * d[:, np.newaxis] - m @ v


def _laplace(key, shape, dtype) -> Array:
  _check_shape("laplace", shape)
  u = uniform(
      key, shape, dtype, minval=-1. + dtypes.finfo(dtype).epsneg, maxval=1.)
  return lax.mul(lax.sign(u), lax.log1p(lax.neg(lax.abs(u))))

