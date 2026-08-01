
def _get_context_mesh(context_mesh: Mesh | AbstractMesh) -> Mesh | AbstractMesh:
  if isinstance(context_mesh, AbstractMesh):
    return context_mesh
  if get_concrete_mesh().empty:
    return context_mesh
  cur_mesh = get_abstract_mesh()
  if cur_mesh.empty or context_mesh.empty:
    return context_mesh
  if cur_mesh == context_mesh.abstract_mesh:
    return context_mesh
  assert context_mesh.size == cur_mesh.size
  return Mesh(context_mesh.devices.reshape(cur_mesh.axis_sizes),
              cur_mesh.axis_names, cur_mesh.axis_types)

