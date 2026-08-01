
def unsafe_get_trace_stack(trace):
  if hasattr(trace, "parent_trace"):
    return unsafe_get_trace_stack(trace.parent_trace) + [trace]
  else:
    return [trace]

