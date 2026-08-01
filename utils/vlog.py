
def vlog(level, msg, *args, **kwargs):
  """Log ``msg % args`` at C++ vlog level ``level``.

  Args:
    level: int, the C++ verbose logging level at which to log the message,
        e.g. 1, 2, 3, 4... While absl level constants are also supported,
        callers should prefer logging.log|debug|info|... calls for such purpose.
    msg: str, the message to be logged.
    *args: The args to be substituted into the msg.
    **kwargs: May contain exc_info to add exception traceback to message.
  """
  log(level, msg, *args, **kwargs)

