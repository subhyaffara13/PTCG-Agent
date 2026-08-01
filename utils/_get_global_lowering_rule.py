
def _get_global_lowering_rule(ctx: LoweringRuleContext, *, what):
  if what.memory_space == gpu_core.GMEM and jnp.issubdtype(
      what.dtype, pallas_core.semaphore
  ):
    collective_axes = tuple(ctx.module_ctx.axis_names)
    return ctx.module_ctx.reserve_semaphores(
        what.shape, collective_axes=collective_axes
    ).__enter__()
  raise NotImplementedError(f"get_global only supports semaphores, got {what}")

