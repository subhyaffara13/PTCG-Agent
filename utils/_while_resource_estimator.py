
def _while_resource_estimator(
    ctx: ResourceEstimatorContext,
    *args,
    cond_jaxpr: jax_core.ClosedJaxpr,
    body_jaxpr: jax_core.ClosedJaxpr,
    **params,
) -> Resources:
  del args, params  # Unused.
  return _estimate_resources(ctx, cond_jaxpr.jaxpr).or_(
      _estimate_resources(ctx, body_jaxpr.jaxpr), ctx.axis_names
  )

