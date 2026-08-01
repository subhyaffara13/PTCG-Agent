
def _get_named_sharding(
    has_named_shardings: bool,
    named_sharding: NamedSharding | None,
    hlo_sharding: HloSharding | None,
    aval: core.ShapedArray,
    new_mesh: mesh_lib.Mesh | mesh_lib.AbstractMesh | None
    ) -> sharding_impls.NamedSharding | None:
  if has_named_shardings:
    if named_sharding is None:  # Unspecified
      return None
    if new_mesh is None:
      return named_sharding
    # TODO(necula): for now we require that the mesh uses the same axis_names
    if (new_mesh.abstract_mesh.axis_sizes != named_sharding.mesh.axis_sizes or
        new_mesh.abstract_mesh.axis_names != named_sharding.mesh.axis_names or
        new_mesh.abstract_mesh.axis_types != named_sharding.mesh.axis_types):
      raise ValueError(f"NamedSharding new mesh {new_mesh} does not match the mesh used for export {named_sharding.mesh}.")

    return named_sharding.update(mesh=new_mesh)

  if hlo_sharding is None:
    return None

  mem_kind: str | None = None
  if aval.memory_space is not None:
    mem_kind = core.mem_space_to_kind(aval.memory_space)

  return sharding_impls.cached_named_sharding(
      new_mesh, sharding_impls.parse_flatten_op_sharding(hlo_sharding, new_mesh)[0],  # pyrefly: ignore[bad-argument-type]
      memory_kind=mem_kind)

