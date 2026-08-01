
def add_manual_axes(axis_ctx: sharding_impls.SPMDAxisContext, sharding, ndim):
  mesh = axis_ctx.mesh.abstract_mesh
  sharding_mesh = sharding.mesh.abstract_mesh
  if (isinstance(sharding, sharding_impls.NamedSharding) and
      sharding_mesh.shape == mesh.shape):
    out_mesh, spec = sharding_mesh, sharding.spec
  else:
    out_mesh, spec = mesh, sharding_impls.parse_flatten_op_sharding(
        sharding._to_xla_hlo_sharding(ndim), mesh)[0]

  out_mesh = out_mesh.update_axis_types(
      {a: AxisType.Manual for a in axis_ctx.manual_axes})
  out = sharding_impls.NamedSharding(out_mesh, spec,
                                     memory_kind=sharding.memory_kind)
  manual_axes = out.mesh.manual_axes
  if any(p in manual_axes for s in out.spec
         if s is not None and s is not PartitionSpec.UNCONSTRAINED
         for p in (s if isinstance(s, tuple) else (s,))):
    raise ValueError(
        f'pspec {out.spec} contains a manual axes {manual_axes} of mesh'
        f' which is not allowed. If you are using a'
        ' with_sharding_constraint under a shard_map, only use the'
        ' mesh axis in PartitionSpec which are not manual.')
  return out

