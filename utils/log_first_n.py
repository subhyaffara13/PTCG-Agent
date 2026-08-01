
def log_first_n(level, msg, n, *args, use_call_stack=False, **kwargs):
  """Logs ``msg % args`` at level ``level`` only first ``n`` times.

  Not threadsafe.

  Args:
    level: int, the absl logging level at which to log.
    msg: str, the message to be logged.
    n: int, the maximal number of times the message is logged.
    *args: The args to be substituted into the msg.
    use_call_stack: bool, whether to include the call stack when counting the
      number of times the message is logged.
    **kwargs: May contain exc_info to add exception traceback to message.
  """
  caller_info = get_absl_logger().findCaller()
  if use_call_stack:
    # To reduce storage costs, we hash the call stack.
    caller_info = (*caller_info[0:3], hash(_fast_stack_trace()))
  count = _get_next_log_count_per_token(caller_info)
  log_if(level, msg, count < n, *args, **kwargs)

