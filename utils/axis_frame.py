
def axis_frame(axis_name):
  return trace_ctx.axis_env.axis_size(axis_name)


def axis_frame() -> PallasGridContext:
  # This is like jax_core.axis_frame, except there should only ever be one
  # active PallasGridAxisName for a particular main_trace because we cannot
  # nest pallas_calls.
  env = _pallas_tracing_env
  assert env.grid_context is not None
  return env.grid_context

