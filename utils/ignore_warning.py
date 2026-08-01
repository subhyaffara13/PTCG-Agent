
def ignore_warning(*, message: str | None = None, category: type = Warning):
  "Context manager that ignores any matching warnings."
  if warnings.showwarning is not _showwarning:
    with warnings.catch_warnings():
      warnings.filterwarnings(
        "ignore", message="" if message is None else message, category=category)
      yield
    return

  if message:
    message_re = re.compile(message)
  else:
    message_re = None

  category_cls = category

  def handler(message, category, filename, lineno, file=None, line=None):
    text = str(message) if isinstance(message, Warning) else message
    if (message_re is None or message_re.match(text)) and issubclass(
        category, category_cls
    ):
      return True
    return False

  _context.handlers.append(handler)
  try:
    yield
  finally:
    _context.handlers.pop()

