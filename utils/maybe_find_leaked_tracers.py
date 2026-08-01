
def maybe_find_leaked_tracers(trace: Trace) -> list[Tracer]:
  """Find the leaked tracers holding a reference to the Trace
  """
  if not getattr(threading.current_thread(), 'pydev_do_not_trace', True):
    warnings.warn(TRACER_LEAK_DEBUGGER_WARNING)
  # Trigger garbage collection to filter out unreachable objects that are alive
  # only due to cyclical dependencies. (We don't care about unreachable leaked
  # tracers since they can't interact with user code and cause a problem.)
  gc.collect()
  tracers = list(filter(lambda x: isinstance(x, Tracer), gc.get_referrers(trace)))
  return tracers

