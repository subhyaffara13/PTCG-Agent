
def _stop_gradient_jvp_rule(primals, tangents):
  # if we don't call stop_gradient here, we'd only peel off one autodiff tracer
  x, = primals
  return stop_gradient(x), ad_util.p2tz(x)

