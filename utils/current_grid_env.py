
def current_grid_env() -> GridEnv | None:
  if not _pallas_tracing_env.grid_env_stack:
    return None
  return _pallas_tracing_env.grid_env_stack[-1]

