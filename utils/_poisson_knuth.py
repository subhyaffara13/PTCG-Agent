
def _poisson_knuth(key, lam, shape, dtype, max_iters) -> Array:
  # Knuth's algorithm for generating Poisson random variates.
  # Reference:
  # https://en.wikipedia.org/wiki/Poisson_distribution#Generating_Poisson-distributed_random_variables

  def body_fn(carry):
    i, k, rng, log_prod = carry
    rng, subkey = _split(rng)
    k = lax.select(log_prod > -lam, k + 1, k)
    u = uniform(subkey, shape, np.float32)
    return i + 1, k, rng, log_prod + jnp.log(u)

  def cond_fn(carry):
    i, log_prod = carry[0], carry[3]
    return (log_prod > -lam).any() & (i < max_iters)

  k_init = lax.full_like(lam, 0, dtype, shape)
  log_rate_init = lax.full_like(lam, 0, np.float32, shape)
  k = lax_control_flow.while_loop(cond_fn, body_fn, (0, k_init, key, log_rate_init))[1]
  return (k - 1).astype(dtype)

