
def _batch_jaxpr_inner(f, store, axis_data, tag, in_axes, *in_vals):
  with core.take_current_trace() as parent_trace:
    trace = BatchTrace(parent_trace, tag, axis_data)
    in_tracers = [BatchTracer(trace, val, dim) if dim is not None else val
                  for val, dim in zip(in_vals, in_axes)]
    # TODO(yashkatariya): Instead of `add_explicit_mesh_axis_names`, we should
    # create a new mesh by removing the axis_data.explicit_mesh_axis from it.
    with (core.set_current_trace(trace),
          core.extend_axis_env_nd([(axis_data.name, axis_data.size)]),
          core.add_spmd_axis_names(axis_data.spmd_name),
          core.add_explicit_mesh_axis_names(axis_data.explicit_mesh_axis)):
      outs = f(*in_tracers)
    out_vals, out_axes = unzip2(map(trace.to_batch_info, outs))
  store.store(out_axes)
  return out_vals

