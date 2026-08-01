
def grid_env(env: GridEnv) -> Generator[None, None, None]:
  _pallas_tracing_env.grid_env_stack.append(env)
  try:
    yield
  finally:
    _pallas_tracing_env.grid_env_stack.pop()

