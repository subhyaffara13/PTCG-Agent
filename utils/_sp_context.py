
def _sp_context(*scalar_prefetch):
  assert _sp_env.scalar_prefetch is None, scalar_prefetch
  _sp_env.scalar_prefetch = scalar_prefetch
  try:
    yield
  finally:
    _sp_env.scalar_prefetch = None

