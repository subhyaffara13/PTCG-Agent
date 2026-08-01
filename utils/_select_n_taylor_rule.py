
def _select_n_taylor_rule(primal_in, series_in, **params):
  b, *cases = primal_in
  primal_out = lax.select_n(b, *cases)
  sel = lambda _, *xs: lax.select_n(b, *xs)
  series_out = [sel(*terms_in) for terms_in in zip(*series_in)]
  return primal_out, series_out

