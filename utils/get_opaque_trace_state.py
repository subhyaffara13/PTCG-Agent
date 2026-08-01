
def get_opaque_trace_state(convention=None):
  del convention
  assert trace_ctx.trace is not None
  return OpaqueTraceState(trace_ctx.trace._weakref)

