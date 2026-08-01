
def record_warnings():
  "Context manager that yields a list of warnings that are raised."
  if warnings.showwarning is not _showwarning:
    with warnings.catch_warnings(record=True) as w:
      warnings.simplefilter("always")
      yield w
    return

  log = []

  def handler(message, category, filename, lineno, file=None, line=None):
    log.append(warnings.WarningMessage(message, category, filename, lineno, file, line))
    return True

  _context.handlers.append(handler)
  try:
    yield log
  finally:
    _context.handlers.pop()

