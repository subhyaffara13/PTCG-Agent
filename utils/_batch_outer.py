
def _batch_outer(f, axis_data, in_dims, *in_vals):
  tag = TraceTag()
  with source_info_util.transform_name_stack('vmap'):
    outs, out_dim_srcs, trace = f(tag, in_dims, *in_vals)
  with core.ensure_no_leaks(trace): del trace
  return outs, out_dim_srcs

