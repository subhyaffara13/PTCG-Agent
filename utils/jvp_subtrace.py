
def jvp_subtrace(f: Callable, tag: core.TraceTag, primals, tangents):
  with core.take_current_trace() as parent_trace:
    trace = JVPTrace(parent_trace, tag)
    in_tracers = [maybe_jvp_tracer(trace, x, t)
                  for x, t in zip(primals, tangents)]
    with core.set_current_trace(trace):
      ans = f(*in_tracers)
    out = unzip2(map(trace.to_primal_tangent_pair, ans))
  return out

