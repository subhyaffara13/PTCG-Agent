
def _binomial_inversion(key, count, prob, shape, dtype, max_iters):
  if config.enable_checks.value:
    assert dtypes.issubdtype(prob.dtype, np.floating)

  log1minusprob = jnp.log1p(-prob)

  def body_fn(carry):
    i, num_geom, geom_sum, key = carry
    subkey, key = split(key)
    num_geom_out = lax.select(geom_sum <= count, num_geom + 1, num_geom)
    u = uniform(subkey, shape, prob.dtype)
    geom = jnp.ceil(jnp.log(u) / log1minusprob)
    geom_sum = geom_sum + geom
    return i + 1, num_geom_out, geom_sum, key

  def cond_fn(carry):
    i, geom_sum = carry[0], carry[2]
    return (geom_sum <= count).any() & (i < max_iters)

  num_geom_init = lax.full_like(prob, 0, prob.dtype, shape)
  geom_sum_init = lax.full_like(prob, 0, prob.dtype, shape)
  carry = (0, num_geom_init, geom_sum_init, key)
  k = lax_control_flow.while_loop(cond_fn, body_fn, carry)[1]
  return (k - 1).astype(dtype)

