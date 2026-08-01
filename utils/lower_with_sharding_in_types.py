
def lower_with_sharding_in_types(ctx, op, aval):
  if aval.sharding.mesh.empty:
    return op
  # Don't emit a wsc under full manual mode to avoid increasing HLO size.
  if aval.sharding.mesh.are_all_axes_manual:
    return op
  if aval.sharding.mesh.are_all_axes_auto:
    return op
  # TODO(yashkatariya): If all the axes in pspec are AUTO or Manual,
  # `return op` early and avoid bloating HLO size.
  if dtypes.issubdtype(aval.dtype, dtypes.extended):
    aval = core.physical_aval(aval)
  if config.use_shardy_partitioner.value:
    proto = aval.sharding._to_sdy_sharding(aval.ndim, modify_wrt_axis_types=True)
    return wrap_with_sharding_op(ctx, op, aval, proto)
  else:
    proto = aval.sharding._to_xla_hlo_sharding(aval.ndim).to_proto()
    unspecified_dims = None
    if aval.sharding.mesh._any_axis_auto:
      unspecified_dims = set(range(aval.ndim))
    return wrap_with_sharding_op(ctx, op, aval, proto, unspecified_dims)

