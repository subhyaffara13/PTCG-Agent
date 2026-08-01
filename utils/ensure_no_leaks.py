
def ensure_no_leaks(trace:Trace):
  yield
  trace.invalidate()
  if config.check_tracer_leaks.value:
    trace_ref = trace._weakref
    del trace
    live_trace = trace_ref()
    if live_trace is not None:
      leaked_tracers = maybe_find_leaked_tracers(live_trace)
      if leaked_tracers:
        raise leaked_tracer_error("trace", live_trace, leaked_tracers)

