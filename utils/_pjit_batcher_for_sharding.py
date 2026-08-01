
def _pjit_batcher_for_sharding(
    s, dim: int, spmd_axis_name: tuple[str, ...] | None,
    mesh, ndim: int):
  if isinstance(s, UnspecifiedValue):
    return s
  hlo_s = s._to_xla_hlo_sharding(ndim)
  if spmd_axis_name is None:
    if sharding_impls.is_hlo_sharding_replicated(hlo_s):
      return s
    if isinstance(s, NamedSharding) and isinstance(s.mesh, AbstractMesh):
      return NamedSharding(
          s.mesh, pxla.batch_spec(s.spec, dim, PartitionSpec.UNCONSTRAINED))
    new_op = hlo_s.to_proto().clone()
    tad = list(new_op.tile_assignment_dimensions)
    tad.insert(dim, 1)
    new_op.tile_assignment_dimensions = tad
    new_gs = GSPMDSharding(s._internal_device_list, new_op)
    return pxla._get_out_sharding_from_orig_sharding([new_gs], [None], s, None)[0]
  else:
    if isinstance(s, NamedSharding) and isinstance(s.mesh, AbstractMesh):
      return NamedSharding(
          s.mesh, pxla.batch_spec(s.spec, dim, spmd_axis_name))
    if isinstance(s, NamedSharding):
      mesh = s.mesh
    if mesh.empty or mesh.is_scalar:
      raise ValueError(
          'If you are using spmd_axis_name parameter of jax.vmap,'
          ' please make sure to run your jitted function inside the mesh'
          ' context manager. Only `jax.lax.with_sharding_constraint` with'
          ' `jax.sharding.NamedSharding` as an input can be transformed with'
          ' spmd_axis_name batching rules outside of an explicit mesh context'
          f' manager scope {s!r}')
    spec = parse_flatten_op_sharding(hlo_s, mesh)[0]
    return NamedSharding(
        mesh, pxla.batch_spec(spec, dim, spmd_axis_name))

