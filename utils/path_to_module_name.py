
def path_to_module_name(path: str) -> str:
  """Normalizes paths to module names."""
  if '/' not in path:  # Already a module name
    return path
  path = path.lstrip('/')
  return (
      path
      .removesuffix('.py')
      .removesuffix('/__init__')
      .replace('/', '.')
  )

