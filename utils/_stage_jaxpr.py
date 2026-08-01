
def _stage_jaxpr(trace: pe.DynamicJaxprTrace, source_info, *tracers,
                 jaxpr: ClosedJaxpr):
  params = dict(call_jaxpr=jaxpr)
  return trace.default_process_primitive(core.closed_call_p, tracers, params,
                                         source_info=source_info)

