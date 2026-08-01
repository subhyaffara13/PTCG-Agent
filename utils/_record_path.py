
def _record_path(name):
  try:
    _error_context.path.append(name)
    yield
  finally:
    _error_context.path.pop()

