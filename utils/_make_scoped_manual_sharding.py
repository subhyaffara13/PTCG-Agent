
def _make_scoped_manual_sharding(ctx, mesh, spec):
  axis_ctx = ctx.module_context.axis_context
  mesh = mesh.abstract_mesh
  if isinstance(axis_ctx, sharding_impls.SPMDAxisContext):
    mesh = mesh.update_axis_types(
        {a: AxisType.Manual for a in axis_ctx.manual_axes})
  return NamedSharding(mesh, spec)

