
def _reduce_resource_estimator(
    ctx: ResourceEstimatorContext, x_aval: jax_core.ShapedArray, *, axes,
    **kwargs
) -> Resources:
  del x_aval, axes, kwargs  # Unused.
  # We don't need SMEM for some reductions, but it depends on the layout, so we
  # conservatively request the maximum scratch space we might need.
  return Resources(smem_scratch_bytes=ctx.reduction_scratch_bytes)

