
def _complex_loggamma_scipy(z: Array) -> Array:
  """Principal branch of the logarithm of the gamma function for complex arguments.

  Matches SciPy's branch cuts (single cut on the negative real axis).
  """
  is_nan = jnp.isnan(z)
  is_pole = (jnp.imag(z) == 0) & (jnp.real(z) == jnp.floor(jnp.real(z))) & (jnp.real(z) <= 0)
  nan_val = jnp.array(complex(jnp.nan, jnp.nan), dtype=z.dtype)

  safe = is_pole | is_nan
  z_safe = jnp.where(safe, jnp.ones_like(z), z)

  n = jnp.maximum(0, jnp.ceil(0.5 - jnp.real(z_safe)).astype(int))

  def cond_fun(state):
    k, _ = state
    return jnp.any(k < n)

  def body_fun(state):
    k, sum_log = state
    mask = k < n
    zk = jnp.where(mask, z_safe + k, jnp.ones_like(z_safe))
    return k + 1, sum_log + jnp.where(mask, jnp.log(zk), jnp.zeros_like(sum_log))

  # Shift z into the right half-plane using loggamma(z) = loggamma(z+n) - sum_{k=0}^{n-1} log(z+k)
  # to match SciPy's branch cuts along the negative real axis.
  _, sum_log = lax.while_loop(cond_fun, body_fun, (0, jnp.zeros_like(z_safe)))

  res = _complex_loggamma(z_safe + n) - sum_log
  return jnp.where(safe, nan_val, res)

