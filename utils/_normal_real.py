
def _normal_real(key, shape, dtype) -> Array:
  _check_shape("normal", shape)
  lo = np.nextafter(np.array(-1., dtype), np.array(0., dtype), dtype=dtype)
  hi = np.array(1., dtype)
  u = uniform(key, shape, dtype, lo, hi)
  return lax.mul(np.array(np.sqrt(2), dtype), lax_special.erf_inv(u))

