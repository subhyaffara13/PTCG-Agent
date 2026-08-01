
def zero_prop(prim, primals_in, series_in, **params):
  primal_out = prim.bind(*primals_in, **params)
  return primal_out, zero_series

