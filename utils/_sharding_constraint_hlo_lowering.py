
def _sharding_constraint_hlo_lowering(ctx, x_node, *, sharding, layout,
                                      context_mesh, unconstrained_dims):
  in_aval, = ctx.avals_in
  out_aval, = ctx.avals_out
  axis_ctx = ctx.module_context.axis_context

  if (isinstance(sharding, NamedSharding) and
      any(o is not None for o in out_aval.sharding.spec)):
    spec = sharding.spec._normalized_spec_for_aval(in_aval.ndim)
    new_spec = []
    for user_spec, aval_spec in zip(spec, out_aval.sharding.spec):
      if aval_spec is None:
        new_spec.append(user_spec)
      else:
        aval_spec = aval_spec if isinstance(aval_spec, tuple) else (aval_spec,)
        if user_spec is PartitionSpec.UNCONSTRAINED:
          raise NotImplementedError
        if user_spec is None:
          new_spec.append(aval_spec)
        elif isinstance(user_spec, tuple):
          new_spec.append(aval_spec + user_spec)
        else:
          new_spec.append(aval_spec + (user_spec,))
    sharding = sharding.update(spec=new_spec)

  if dtypes.issubdtype(in_aval.dtype, dtypes.extended):
    in_aval = core.physical_aval(in_aval)
  if (isinstance(axis_ctx, sharding_impls.SPMDAxisContext) and
      axis_ctx.manual_axes):
    sharding = mlir.add_manual_axes(axis_ctx, sharding, in_aval.ndim)
  if config.use_shardy_partitioner.value:
    sharding = sharding._to_sdy_sharding(in_aval.ndim)
  else:
    sharding = sharding._to_xla_hlo_sharding(in_aval.ndim).to_proto()
  out = mlir.wrap_with_sharding_op(
      ctx, x_node, out_aval, sharding, unspecified_dims=unconstrained_dims)
  if layout is not None:
    out = mlir.wrap_with_layout_op(ctx, out, out_aval, layout, in_aval)
  return [out]

