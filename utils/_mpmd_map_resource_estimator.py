
def _mpmd_map_resource_estimator(
    ctx: ResourceEstimatorContext, *args, jaxprs: tuple[jax_core.Jaxpr, ...],
    **params
) -> Resources:
  del args, params  # Unused.
  if len(jaxprs) > 1:
    raise NotImplementedError(
        "MPMD map with multiple jaxprs not supported for resource estimation."
    )
  return _estimate_resources(ctx, jaxprs[0])

