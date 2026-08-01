
def _run_state_resource_estimator(
    ctx: ResourceEstimatorContext, *args, jaxpr: jax_core.Jaxpr, **params
) -> Resources:
  del args, params  # Unused.
  return _estimate_resources(ctx, jaxpr)

