
def _truncated_normal(key, lower, upper, shape, dtype) -> Array:
  if shape is None:
    shape = lax.broadcast_shapes(np.shape(lower), np.shape(upper))
  else:
    _check_shape("truncated_normal", shape, np.shape(lower), np.shape(upper))

  sqrt2 = np.array(np.sqrt(2), dtype)
  lower = lax.convert_element_type(lower, dtype)
  upper = lax.convert_element_type(upper, dtype)
  a = lax_special.erf(lower / sqrt2)
  b = lax_special.erf(upper / sqrt2)
  if not dtypes.issubdtype(dtype, np.floating):
    raise TypeError("truncated_normal only accepts floating point dtypes.")
  u = uniform(key, shape, dtype, minval=a, maxval=b)
  out = sqrt2 * lax_special.erf_inv(u)
  # Clamp the value to the open interval (lower, upper) to make sure that
  # rounding (or if we chose `a` for `u`) doesn't push us outside of the range.
  return jnp.clip(
      out,
      lax.nextafter(lax.stop_gradient(lower), np.array(np.inf, dtype=dtype)),
      lax.nextafter(lax.stop_gradient(upper), np.array(-np.inf, dtype=dtype)))

