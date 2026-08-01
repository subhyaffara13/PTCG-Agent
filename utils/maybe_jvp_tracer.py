
def maybe_jvp_tracer(trace, primal, tangent):
  if (type(tangent) is Zero or
      isinstance(typeof(tangent), core.ShapedArray)
      and dtype(tangent) == float0):
    return primal
  else:
    return JVPTracer(trace, primal, tangent)

