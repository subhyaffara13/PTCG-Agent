
def get_abstract_mesh() -> AbstractMesh:
  val = jax_config.abstract_mesh_context_manager.value
  return empty_abstract_mesh if val is None else val

