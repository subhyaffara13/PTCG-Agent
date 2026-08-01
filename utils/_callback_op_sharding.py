
def _callback_op_sharding(
    axis_context, sharding: Sharding | None, avals_out
):
  if isinstance(axis_context, sharding_impls.SPMDAxisContext):
    # If we have fully manual sharding during lowering, that means the JAX
    # program has per-device semantics, so we run the callback on each device.
    if axis_context.manual_axes != frozenset(axis_context.mesh.axis_names):
      raise NotImplementedError(
          "callbacks are only supported in spmd computations when all mesh"
          " axes are partitioned manually (no partial automatic sharding)."
      )
    if sharding is not None:
      raise NotImplementedError(
          "callbacks do not support specifying sharding inside spmd"
          " computations"
      )
    if config.use_shardy_partitioner.value:
      op_sharding = _get_sdy_array_list_for_callbacks(avals_out)
    else:
      op_sharding = xc.OpSharding()
      op_sharding.type = xc.OpSharding.Type.MANUAL
    return op_sharding

  if isinstance(axis_context, sharding_impls.ShardingContext):
    if sharding is not None:
      if (isinstance(sharding, sharding_impls.NamedSharding) and
          sharding.mesh.is_scalar):  # pyrefly: ignore[missing-attribute]
        pass
      elif not isinstance(sharding, SingleDeviceSharding):
        raise NotImplementedError(
            "pure_callback only supports SingleDeviceSharding, but got"
            f" {type(sharding)}"
        )
      device = next(iter(sharding.device_set))
      device_assignment = axis_context.device_assignment
      if device_assignment is None:
        raise AssertionError(
            "Please file a bug at https://github.com/jax-ml/jax/issues")
      try:
        device_index = device_assignment.index(device)
      except IndexError as e:
        raise ValueError(
            "Sharding provided to pure_callback specifies a device"
            f" {device} that is not in the device assignment"
            f" ({device_assignment})") from e
    else:
      device_index = 0

    # If we have fully automatic sharding during lowering, that means the JAX
    # program has bulk array semantics, so we run the callback with a MAXIMAL
    # sharding and hence execute it only once on the full logical value).
    if config.use_shardy_partitioner.value:
      # For shardy, we need to have the same number of shardy annotations as the
      # number of result ops. If there are no result ops, we need 1 shardy
      # annotation.
      num_sdy_shardings = max(1, len(avals_out))
      op_sharding = SdyArrayList((
          SdyArray(mesh_shape=(), dim_shardings=(),
                   logical_device_ids=(device_index,)),) * num_sdy_shardings)
    else:
      op_sharding = xc.OpSharding()
      op_sharding.type = xc.OpSharding.Type.MAXIMAL
      op_sharding.tile_assignment_dimensions = [1]
      op_sharding.tile_assignment_devices = [device_index]
    return op_sharding

  # When there's no SPMD partitioning going on, don't annotate a sharding.
  return None

