
def tracing_grid_env(grid: GridMappingGrid, mapped_dims: tuple[int, ...]):
  if dynamic_shapes_export_enabled():
    assert all(i is dynamic_grid_dim or jax_core.is_dim(i) for i in grid)
  else:
    assert all(i is dynamic_grid_dim or isinstance(i, int) for i in grid)
  old_grid_context = _pallas_tracing_env.grid_context
  try:
    _pallas_tracing_env.grid_context = PallasGridContext(grid, mapped_dims)
    yield
  finally:
    _pallas_tracing_env.grid_context = old_grid_context

