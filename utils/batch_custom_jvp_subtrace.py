
def batch_custom_jvp_subtrace(f, store, tag, axis_data, in_dims, *in_vals):
  with core.take_current_trace() as parent_trace:
    trace = BatchTrace(parent_trace, tag, axis_data)
    in_tracers = [val if dim is None else
                  SymbolicZero(core.mapped_aval(axis_data.size, dim, val.aval))
                  if type(val) is SymbolicZero else BatchTracer(trace, val, dim)
                  for val, dim in zip(in_vals, in_dims * 2)]
    with core.set_current_trace(trace):
      out_tracers: list[BatchTracer | SymbolicZero] = f(*in_tracers)
  out_vals, out_dims = unzip2(map(trace.to_batch_info, out_tracers))
  out_primals, out_tangents = split_list(out_vals, [len(out_vals) // 2])
  out_primal_bds, out_tangent_bds = split_list(out_dims, [len(out_vals) // 2])
  out_dims = map(_merge_bdims, out_primal_bds, out_tangent_bds)
  out_primals  = map(partial(matchaxis, axis_data), out_primal_bds, out_dims,
                     out_primals)
  out_tangents = map(partial(_matchaxis_symzeros, axis_data),
                     out_tangent_bds, out_dims, out_tangents)
  store.store(out_dims)
  return out_primals + out_tangents

