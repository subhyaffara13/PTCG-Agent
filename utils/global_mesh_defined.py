
def global_mesh_defined() -> bool:
  """Checks if global mesh resource environment is defined."""
  mesh = get_global_mesh()
  return mesh is not None

