
def _owens_t_impl(h, a):
  h = jnp.abs(h)
  abs_a = jnp.abs(a)
  root_2 = _lax_const(h, np.sqrt(2))
  h_normed = h / root_2

  modified_a = jnp.where(abs_a <= 1., abs_a, jnp.reciprocal(abs_a))
  modified_h = jnp.where(abs_a <= 1., h, abs_a * h)

  result = _owens_t_quadrature(modified_h, modified_a)

  # Exact values for h=0 and a=1
  result = jnp.where(modified_h == 0., arctan(modified_a) / (2 * np.pi), result)
  result = jnp.where(
      modified_a == 1.,
      0.125 * lax.erfc(-modified_h / root_2) * lax.erfc(modified_h / root_2),
      result)

  # Reciprocal correction for |a| > 1
  normh = lax.erfc(h_normed)
  normah = lax.erfc(abs_a * h_normed)
  result = jnp.where(
      abs_a > 1.,
      jnp.where(
          abs_a * h <= 0.67,
          (0.25 - 0.25 * lax.erf(h_normed) * lax.erf(abs_a * h_normed)
           - result),
          0.25 * (normh + normah - normh * normah) - result),
      result)

  result = lax.sign(a) * result
  return jnp.where(jnp.isnan(a) | jnp.isnan(h), jnp.full_like(result, jnp.nan), result)

