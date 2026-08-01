
def _jaxpr_call_resource_estimator(
    ctx: ResourceEstimatorContext,
    *args,
    jaxpr: jax_core.Jaxpr,
    **params
):
  del args, params  # Unused.
  return _estimate_resources(ctx, jaxpr)

