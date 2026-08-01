
def _chisquare(key, df, shape, dtype, out_sharding) -> Array:
  df = lax.convert_element_type(df, dtype)
  two = lax._const(df, 2)
  half_df = lax.div(df, two)
  log_g = loggamma(key, a=half_df, shape=shape, dtype=dtype, out_sharding=out_sharding)
  chi2 = lax.mul(jnp.exp(log_g), two)
  return chi2

