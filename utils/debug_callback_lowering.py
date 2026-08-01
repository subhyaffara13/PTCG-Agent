
def debug_callback_lowering(ctx, *args, effect, partitioned, callback, **params):
  axis_context = ctx.module_context.axis_context
  if isinstance(axis_context, sharding_impls.SPMDAxisContext):
    # We're a shard_map, which might be partial-manual or full-manual.
    partial_auto = set(axis_context.mesh.axis_names) - axis_context.manual_axes
    if partial_auto:
      # If we have partial manual / partial auto sharding, we gather and
      # conditionally run the callback.
      lower = partial(
          _debug_callback_partial_auto,
          axis_context,
          effect=effect,
          partitioned=partitioned,
          callback=callback,
          **params,
      )
      return mlir.lower_fun(lower)(ctx, *args)
    elif set(axis_context.manual_axes) == set(axis_context.mesh.axis_names):
      # If we have fully manual sharding during lowering, that means the JAX
      # program has per-device semantics, so we run the callback on each device.
      if config.use_shardy_partitioner.value:
        sharding = cb._get_sdy_array_list_for_callbacks(ctx.avals_out)
      else:
        sharding = xc.OpSharding()
        sharding.type = xc.OpSharding.Type.MANUAL
    else:
      assert False  # Unreachable
  elif isinstance(axis_context, sharding_impls.ShardingContext):
    # If we have fully automatic sharding during lowering, that means the JAX
    # program has bulk array semantics, so we run the callback with a MAXIMAL
    # sharding and hence execute it only once on the full logical value).
    if config.use_shardy_partitioner.value:
      sharding = sharding_impls.SdyArrayList((
          sharding_impls.SdyArray(
              mesh_shape=(), dim_shardings=(), logical_device_ids=(0,)),))
    else:
      sharding = xc.OpSharding()
      sharding.type = xc.OpSharding.Type.MAXIMAL
      sharding.tile_assignment_dimensions = [1]
      sharding.tile_assignment_devices = [0]
  else:
    # When there's no SPMD partitioning going on, don't annotate a sharding.
    sharding = None

  def _callback(*flat_args):
    debug_callback_p.impl(
        *flat_args,
        effect=effect,
        partitioned=partitioned,
        callback=callback,
        **params,
    )
    return ()
  if effects.ordered_effects.contains(effect):
    token = ctx.tokens_in.get(effect)
    result, token, _ = cb.emit_python_callback(
        ctx, _callback, token, list(args), ctx.avals_in, ctx.avals_out,
        has_side_effect=True, returns_token=True, partitioned=partitioned)
    ctx.set_tokens_out(
        ctx.tokens_in.update_tokens(mlir.TokenSet({effect: token})))
  else:
    result, _, _ = cb.emit_python_callback(
        ctx, _callback, None, list(args), ctx.avals_in, ctx.avals_out,
        has_side_effect=True, returns_token=True, partitioned=partitioned,
        sharding=sharding)
  return result

