
def cur_qdd(x):
  prev_trace = trace_ctx.trace
  trace_ctx.set_trace(eval_trace)
  try:
    return prev_trace.cur_qdd(x)
  finally:
    trace_ctx.set_trace(prev_trace)

