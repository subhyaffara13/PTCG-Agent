
def mpmd_map_tracing_context(
  mesh: pallas_core.Mesh,
  other_meshes: tuple[pallas_core.Mesh, ...],
) -> Generator[None, None, None]:
  super_mesh_shape = get_super_mesh_shape(other_meshes)
  with (
      mesh.tracing_context(),
      jax_core.extend_axis_env_nd(super_mesh_shape.items()),
      config._check_vma(False),
  ):
    yield

