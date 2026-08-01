
def _internal_use_concrete_mesh(mesh: Mesh):
  assert isinstance(mesh, Mesh)
  prev_val = config.device_context.swap_local(mesh)
  try:
    yield
  finally:
    config.device_context.set_local(prev_val)

