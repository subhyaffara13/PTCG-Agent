import logging

def _disable_all_debug_logging():
  """Disables all debug logging enabled via `enable_debug_logging`.

  The default logging behavior will still be in effect, i.e. WARNING and above
  will be logged to stderr without extra message formatting.
  """
  for logger, prev_level in _debug_enabled_loggers:
    logger: logging.Logger
    logger.removeHandler(_debug_handler)
    logger.setLevel(prev_level)
  _debug_enabled_loggers.clear()

