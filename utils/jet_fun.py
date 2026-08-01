
def jet_fun(f, order, primals, series):
  tag = core.TraceTag()
  out_primals, out_terms = f(tag, order, primals, series)
  out_terms = [[jnp.zeros_like(p)] * order if s is zero_series else s
               for p, s in zip(out_primals, out_terms)]
  return out_primals, out_terms

