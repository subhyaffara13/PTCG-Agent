
def log_if(level, msg, condition, *args, **kwargs):
  """Logs ``msg % args`` at level ``level`` only if condition is fulfilled."""
  if condition:
    log(level, msg, *args, **kwargs)

