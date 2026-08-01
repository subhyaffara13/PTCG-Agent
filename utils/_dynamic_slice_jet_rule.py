
def _dynamic_slice_jet_rule(primals_in, series_in, **params):
  operand, *start_indices = primals_in
  primal_out = lax.dynamic_slice_p.bind(operand, *start_indices, **params)
  series_out = [lax.dynamic_slice_p.bind(terms_in[0], *start_indices, **params)
                for terms_in in zip(*series_in)]
  return primal_out, series_out

