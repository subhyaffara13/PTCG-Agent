
def _resolve_mesh(*meshes) -> mesh_lib.AbstractMesh:
  """Resolves the mesh between given meshes."""
  unique_meshes = {mesh for mesh in meshes if not mesh.empty}
  if len(unique_meshes) > 1:
    raise core.ShardingTypeError(
        f"Conflicting meshes received. Got: {unique_meshes=}"
    )
  if not unique_meshes:
    return mesh_lib.get_abstract_mesh()
  mesh, = unique_meshes
  return mesh

