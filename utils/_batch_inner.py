from typing import Callable

def _batch_inner(f: Callable, axis_data, out_dim_dests, sum_match, tag, in_dims, *in_vals):
  in_dims = in_dims() if callable(in_dims) else in_dims
  with core.take_current_trace() as parent_trace:
    trace = BatchTrace(parent_trace, tag, axis_data)
    idx = memoize(lambda: BatchTracer(trace, make_iota(axis_data.size), 0,
                                      source_info_util.current()))
    with core.set_current_trace(parent_trace):
      in_tracers = map(partial(to_elt, trace, idx), in_vals, in_dims)  # pyrefly: ignore[bad-argument-type]  # pyrefly#2385
    # TODO(yashkatariya): Instead of `add_explicit_mesh_axis_names`, we should
    # create a new mesh by removing the axis_data.explicit_mesh_axis from it.
    with (core.set_current_trace(trace),
          core.extend_axis_env_nd([(axis_data.name, axis_data.size)]),
          core.add_spmd_axis_names(axis_data.spmd_name),
          core.add_explicit_mesh_axis_names(axis_data.explicit_mesh_axis)):
      outs = f(*in_tracers)
      out_dim_dests = out_dim_dests() if callable(out_dim_dests) else out_dim_dests
      out_vals, out_dim_srcs = unzip2(
          map(partial(from_elt, trace, axis_data.size, axis_data.explicit_mesh_axis, sum_match),
              range(len(outs)), outs, out_dim_dests))  # pyrefly: ignore[bad-argument-type]  # pyrefly#2385
  return out_vals, out_dim_srcs, trace

