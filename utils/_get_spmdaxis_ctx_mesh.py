
def _get_spmdaxis_ctx_mesh(mesh):
  if isinstance(mesh, AbstractMesh):
    concrete_mesh = get_concrete_mesh()
    return concrete_mesh if not concrete_mesh.empty else mesh
  return mesh

