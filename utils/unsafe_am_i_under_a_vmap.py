
def unsafe_am_i_under_a_vmap() -> bool:
  return 'BatchTrace' in str(unsafe_get_trace_stack(trace_ctx.trace))

