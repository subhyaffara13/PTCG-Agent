
def exception(msg, *args, exc_info=True, **kwargs):
  """Logs an exception, with traceback and message."""
  error(msg, *args, exc_info=exc_info, **kwargs)

