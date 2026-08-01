
def _get_abstract_mesh_from_avals(in_avals) -> mesh_lib.AbstractMesh:
  m = None
  for a in in_avals:
    if a is core.abstract_token:
      continue
    if a.sharding.mesh.empty:
      continue
    if m is not None and m != a.sharding.mesh:
      if m.are_all_axes_auto and a.sharding.mesh.are_all_axes_auto:
        return mesh_lib.empty_abstract_mesh
      raise ValueError(
          f'Mesh for all inputs should be equal. Got one mesh: {m} and'
          f' another mesh: {a.sharding.mesh}')
    m = a.sharding.mesh
  return mesh_lib.empty_abstract_mesh if m is None else m

