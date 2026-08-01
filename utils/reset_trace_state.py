
def reset_trace_state() -> bool:
  """Resets the global trace state and returns True if it was already clean."""
  if not trace_ctx.is_top_level():
    trace_ctx.reset()
    return False
  else:
    return True

