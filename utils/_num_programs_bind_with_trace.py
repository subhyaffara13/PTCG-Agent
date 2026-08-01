
def _num_programs_bind_with_trace(trace, _, avals, params):
  axis = params.pop("axis")
  # We might be using a local grid env
  grid_env = pallas_core.current_grid_env()
  if grid_env:
    return grid_env[axis].size
  # Otherwise, we look up the size of the grid in the axis env
  frame = pallas_core.axis_frame()
  size = frame.size(axis)
  if size is pallas_core.dynamic_grid_dim:
    return jax_core.Primitive.bind_with_trace(num_programs_p, trace, (), avals,
                                              dict(axis=axis))
  return size

