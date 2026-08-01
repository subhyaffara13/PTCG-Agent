
def unsafe_am_i_under_a_jit() -> bool:
  return 'DynamicJaxprTrace' in str(unsafe_get_trace_stack(trace_ctx.trace))

