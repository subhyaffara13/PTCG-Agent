
def get_super_mesh_shape(
    meshes: Iterable[pallas_core.Mesh],
) -> Mapping[str, int]:
  super_mesh_shape = {}
  for mesh in meshes:
    for k, v in mesh.shape.items():
      # An extra check since `check_is_compatible_with` should catch it.
      assert (
          k not in super_mesh_shape or super_mesh_shape[k] == v
      ), f"Conflicting size for axis {k}"
      super_mesh_shape[k] = v
  return super_mesh_shape

