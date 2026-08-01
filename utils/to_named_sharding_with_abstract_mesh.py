
def to_named_sharding_with_abstract_mesh(
    s: LoweringSharding,
    aval: core.ShapedArray,
    mesh: mesh_lib.Mesh | mesh_lib.AbstractMesh | None) -> NamedSharding | None:
  # We store and serialize all shardings as NamedShardings with abstract mesh,
  # even if they are SingleDeviceShardings.
  if isinstance(s, sharding_impls.UnspecifiedValue):
    return None
  if isinstance(s, sharding_impls.NamedSharding):
    if isinstance(s.mesh, mesh_lib.Mesh) and s.mesh.is_scalar:
      return sharding_impls.NamedSharding(
          s.mesh.abstract_mesh,
          sharding_impls.PartitionSpec(*([None] *aval.ndim)),
          memory_kind=s.memory_kind)
    return sharding_impls.NamedSharding(s.mesh.abstract_mesh,
                                        s.spec, memory_kind=s.memory_kind)
  if isinstance(s, sharding_impls.SingleDeviceSharding):
    return sharding_impls.NamedSharding(
      mesh_lib.empty_abstract_mesh,
      sharding_impls.PartitionSpec(*([None] *aval.ndim)),
      memory_kind=s.memory_kind)

  if isinstance(s, sharding_impls.GSPMDSharding):
    if mesh is None:
      if s._hlo_sharding.tuple_elements():
        raise TypeError(
            f"Cannot convert GSPMDSharding {s} into NamedSharding.")
      elif s._hlo_sharding.is_replicated():
        return sharding_impls.NamedSharding(
            mesh_lib.empty_abstract_mesh,
            sharding_impls.PartitionSpec(*([None] *aval.ndim)),
            memory_kind=s.memory_kind)
      elif s._hlo_sharding.is_tiled():
        if not s._hlo_sharding.is_tile_assignment_iota():
          raise TypeError(
              f"Cannot convert GSPMDSharding {s} into NamedSharding.")
        axis_sizes = tuple(s._hlo_sharding.get_axis_sizes())
        axis_names = tuple(f'_axis_{i}' for i in range(len(axis_sizes)))
        mesh = mesh_lib.AbstractMesh(axis_sizes, axis_names)
        return sharding_impls._gspmd_to_named_sharding_via_mesh(s, mesh)
      else:
        raise TypeError(
            f"Cannot convert GSPMDSharding {s} into NamedSharding.")
    else:
      return sharding_impls._gspmd_to_named_sharding_via_mesh(s, mesh)

  assert False, f"Unsupported sharding: {s}"

