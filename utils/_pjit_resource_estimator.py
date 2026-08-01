
def _pjit_resource_estimator(
    ctx: ResourceEstimatorContext,
    *args,
    jaxpr: jax_core.ClosedJaxpr,
    **params,
) -> Resources:
  del args, params  # Unused.
  return _estimate_resources(ctx, jaxpr.jaxpr)

