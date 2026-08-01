
def linear_prop(prim, primals_in, series_in, **params):
  primal_out = prim.bind(*primals_in, **params)
  series_out = [prim.bind(*terms_in, **params) for terms_in in zip(*series_in)]
  if prim.multiple_results:
    series_out = safe_zip(*series_out)
  return primal_out, series_out

