import logging
import sys

def use_absl_handler():
  """Uses the ABSL logging handler for logging.

  This method is called in :func:`app.run()<absl.app.run>` so the absl handler
  is used in absl apps.
  """
  global _attempted_to_remove_stderr_stream_handlers
  if not _attempted_to_remove_stderr_stream_handlers:
    # The absl handler logs to stderr by default. To prevent double logging to
    # stderr, the following code tries its best to remove other handlers that
    # emit to stderr. Those handlers are most commonly added when
    # logging.info/debug is called before calling use_absl_handler().
    handlers = [
        h for h in logging.root.handlers
        if isinstance(h, logging.StreamHandler) and h.stream == sys.stderr]
    for h in handlers:
      logging.root.removeHandler(h)
    _attempted_to_remove_stderr_stream_handlers = True

  absl_handler = get_absl_handler()
  if absl_handler not in logging.root.handlers:
    logging.root.addHandler(absl_handler)
    FLAGS['verbosity']._update_logging_levels()  # pylint: disable=protected-access
    FLAGS['logger_levels']._update_logger_levels()  # pylint: disable=protected-access

