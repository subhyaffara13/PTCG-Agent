
def _closed_call_resource_estimator(ctx, *args, call_jaxpr):
  del args  # Unused.
  if call_jaxpr.consts: raise NotImplementedError
  return lowering._estimate_resources(ctx, call_jaxpr.jaxpr)

