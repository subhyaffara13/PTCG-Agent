
def raise_on_warnings():
  "Context manager that raises an exception if a warning is raised."
  if warnings.showwarning is not _showwarning:
    with warnings.catch_warnings():
      warnings.simplefilter("error")
      yield
    return

  def handler(message, category, filename, lineno, file=None, line=None):
    raise category(message)

  _context.handlers.append(handler)
  try:
    yield
  finally:
    _context.handlers.pop()

