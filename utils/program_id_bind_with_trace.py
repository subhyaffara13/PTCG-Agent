
def program_id_bind_with_trace(trace, _, avals, params):
  axis = params.pop("axis")
  grid_env = pallas_core.current_grid_env()
  if grid_env:
    return grid_env[axis].index
  frame = pallas_core.axis_frame()
  # Query the size of the axis to make sure it's a valid axis (and error
  # otherwise).
  _ = frame.size(axis)
  return jax_core.Primitive.bind_with_trace(program_id_p, trace, (), avals,
                                            dict(axis=axis))

