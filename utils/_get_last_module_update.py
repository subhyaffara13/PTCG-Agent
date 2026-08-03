import sys

def _get_last_module_update(module_name: str) -> int | None:
  """Get the last update for one module."""
  module = sys.modules.get(module_name, None)
  if module is None:
    return None
  if module.__name__ == '__main__':
    return None

  module_file = getattr(module, '__file__', None)
  if not module_file:
    return None

  module_file = epath.Path(module_file)

  try:
    return module_file.stat().mtime
  except OSError:
    return None

