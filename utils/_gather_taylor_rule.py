
def _gather_taylor_rule(primals_in, series_in, **params):
  operand, start_indices = primals_in
  gs, _ = series_in
  primal_out = lax.gather_p.bind(operand, start_indices, **params)
  series_out = [lax.gather_p.bind(g, start_indices, **params) for g in gs]
  return primal_out, series_out

