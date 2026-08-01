
def batch_subtrace(f, store, tag, axis_data, in_dims, *in_vals):
  with core.take_current_trace() as parent_trace:
    trace = BatchTrace(parent_trace, tag, axis_data)
    with core.set_current_trace(trace):
      in_dims = in_dims() if callable(in_dims) else in_dims
      in_tracers = [BatchTracer(trace, x, dim, source_info_util.current())
                    if dim is not None else x for x, dim in zip(in_vals, in_dims)]  # pyrefly: ignore[bad-argument-type]  # pyrefly#2385
      outs = f(*in_tracers)
    out_vals, out_dims = unzip2(map(trace.to_batch_info, outs))
  store.store(out_dims)
  return out_vals

