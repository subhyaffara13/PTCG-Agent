
def _tpu_gpu_device_put_lowering(ctx, *xs, devices, srcs, copy_semantics):
  # TODO(yashkatariya): Maybe we should add the custom calls anyways if it's
  # being used inside jit? Atleast for now, this preserves the old behavior.
  if ctx.module_context.all_default_mem_kind:
    return xs
  def lower(x, device, aval, out_aval):
    if ((isinstance(device, Sharding) and device.memory_kind is not None) or
        isinstance(device, core.MemorySpace)):
      if isinstance(device, Sharding):
        if config.use_shardy_partitioner.value:
          x = mlir.wrap_with_sharding_op(
              ctx, x, out_aval,
              device._to_sdy_sharding(aval.ndim))
        else:
          x = mlir.wrap_with_sharding_op(
              ctx, x, out_aval,
              device._to_xla_hlo_sharding(aval.ndim).to_proto())
      mem_kind = (core.mem_space_to_kind(device)
                  if isinstance(device, core.MemorySpace) else device.memory_kind)
      assert mem_kind is not None
      x = mlir.wrap_with_memory_kind(ctx.module_context, x, mem_kind, out_aval)
      return x
    return x
  return list(map(lower, xs, devices, ctx.avals_in, ctx.avals_out))

