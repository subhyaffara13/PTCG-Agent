import logging

def _showwarning(
    message: Warning | str,
    category: type[Warning],
    filename: str,
    lineno: int,
    file: TextIO | None = None,
    line: str | None = None,
) -> None:
    if file is not None:
        if _original_showwarning is not None:
            _original_showwarning(message, category, filename, lineno, file, line)
    elif issubclass(category, PipDeprecationWarning):
        # We use a specially named logger which will handle all of the
        # deprecation messages for pip.
        logger = logging.getLogger("pip._internal.deprecations")
        if isinstance(message, PipDeprecationWarning) and message.include_source:
            logger.warning("%s (%s:%s)", message, filename, lineno)
        else:
            logger.warning(message)
    else:
        _original_showwarning(message, category, filename, lineno, file, line)


def _showwarning(message, category, filename, lineno, file=None, line=None):
  for handler in reversed(_context.handlers):
    if handler(message, category, filename, lineno, file, line):
      return
  raise category(message)

