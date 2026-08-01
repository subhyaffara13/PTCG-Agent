
def sanitize_name(name: str) -> str:
  """Ensure a name is usable as module or function name."""
  return _module_name_regex.sub("_", name)

