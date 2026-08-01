
def _match_axes_and_sum(f, axis_data, out_dims_thunk, out_dim_dests, *in_vals):
  # this is like _match_axes, but we do reduce-sums as needed
  out_vals = f(*in_vals)
  return map(partial(_matchaxis_symzeros, axis_data, sum_match=True),
             out_dims_thunk(), out_dim_dests, out_vals)

