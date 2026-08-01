
def replica_count(
    global_mesh: jax.sharding.Mesh, *, replica_axis_index: int = 0
) -> int:
  """Number of slices implied by the mesh's replica dimension."""
  if len(global_mesh.shape_tuple) == 1:
    return 1
  return global_mesh.devices.shape[replica_axis_index]

