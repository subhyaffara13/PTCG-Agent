
def _get_global_resource_estimator(
    ctx: ResourceEstimatorContext, *, what
) -> Resources:
  if what.memory_space == gpu_core.GMEM and jnp.issubdtype(
      what.dtype, pallas_core.semaphore
  ):
    collective_axes = tuple(ctx.axis_names)
    return Resources(scoped_gmem_semaphores={collective_axes: what.size})
  raise NotImplementedError(f"get_global only supports semaphores, got {what}")

