
def _stop_gradient(x):
  if dtypes.issubdtype(core.typeof(x).dtype, dtypes.extended):
    return x
  elif isinstance(x, ad.JVPTracer):
    return _stop_gradient(x.primal)
  else:
    return ad_util.stop_gradient_p.bind(x)

