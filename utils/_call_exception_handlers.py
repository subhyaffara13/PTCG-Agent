import logging

def _call_exception_handlers(exception):
  """Calls any installed exception handlers."""
  for handler in EXCEPTION_HANDLERS:
    try:
      if handler.wants(exception):
        handler.handle(exception)
    except:  # pylint: disable=bare-except
      try:
        # We don't want to stop for exceptions in the exception handlers but
        # we shouldn't hide them either.
        logging.error(traceback.format_exc())
      except:  # pylint: disable=bare-except
        # In case even the logging statement fails, ignore.
        pass

