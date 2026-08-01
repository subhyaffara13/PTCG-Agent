
def _cond_resource_estimator(
    ctx: ResourceEstimatorContext, *args, branches
) -> Resources:
  del args  # Unused.
  return functools.reduce(
      lambda a, b: a.or_(b, ctx.axis_names),
      (_estimate_resources(ctx, branch.jaxpr) for branch in branches),
  )

