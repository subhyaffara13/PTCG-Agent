
def fatal(msg, *args, **kwargs):
  # type: (Any, Any, Any) -> NoReturn
  """Logs a fatal message."""
  log(FATAL, msg, *args, **kwargs)

