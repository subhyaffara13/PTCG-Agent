
def _abs_taylor_rule(x, series_in, **params):
  x, = x
  zero = lax.full_like(x, 0, shape=())
  primal_out = lax.abs_p.bind(x, **params)
  negs = lax.select(lax.lt(x, zero), lax.full_like(x, -1), lax.full_like(x, 1.0))
  fix_sign = lambda y: negs * y
  series_out = [fix_sign(*terms_in, **params) for terms_in in zip(*series_in)]
  return primal_out, series_out

