
def _integer_pow_taylor(primals_in, series_in, *, y):
  if y == 0:
    return jet2(jnp.ones_like, primals_in, series_in)
  else:
    return jet2(lambda x: _pow_by_squaring(x, y), primals_in, series_in)

