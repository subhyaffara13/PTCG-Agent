
def log_every_n_seconds(
    level, msg, n_seconds, *args, use_call_stack=False, **kwargs
):
  """Logs ``msg % args`` at level ``level`` iff ``n_seconds`` elapsed since last call.

  Logs the first call, logs subsequent calls if 'n' seconds have elapsed since
  the last logging call from the same call site (file + line). Not thread-safe.

  Args:
    level: int, the absl logging level at which to log.
    msg: str, the message to be logged.
    n_seconds: float or int, seconds which should elapse before logging again.
    *args: The args to be substituted into the msg.
    use_call_stack: bool, whether to include the call stack when counting the
      number of times the message is logged.
    **kwargs: May contain exc_info to add exception traceback to message.
  """
  caller_info = get_absl_logger().findCaller()
  if use_call_stack:
    # To reduce storage costs, we hash the call stack.
    caller_info = (*caller_info[0:3], hash(_fast_stack_trace()))
  should_log = _seconds_have_elapsed(caller_info, n_seconds)
  log_if(level, msg, should_log, *args, **kwargs)

