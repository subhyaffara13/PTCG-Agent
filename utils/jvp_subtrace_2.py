
def jvp_subtrace_2(f: Callable, tag: core.TraceTag, primals, tangents):
  with core.take_current_trace() as parent_trace:
    trace = JVPTrace(parent_trace, tag)
    in_tracers = [maybe_jvp_tracer(trace, x, t)
                  for x, t in zip(primals, tangents)]
    with core.set_current_trace(trace):
      ans = f(*in_tracers)
  return ans.map(trace.to_primal_tangent_pair).unzip2()

