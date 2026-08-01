
def _dynamic_update_slice_jet_rule(primals_in, series_in, **params):
  operand, update, *start_indices = primals_in
  primal_out = lax.dynamic_update_slice_p.bind(operand, update, *start_indices)
  series_out = [lax.dynamic_update_slice_p.bind(*terms_in[:2], *start_indices, **params)
                for terms_in in zip(*series_in)]
  return primal_out, series_out

