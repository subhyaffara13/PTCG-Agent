
def _extract_captures(module, state, var_types):
  """Extract intermediates from __captures__ tuple into state dict."""
  for path, mod in iter_modules(module):
    if hasattr(mod, '__captures__'):
      captures_tuple = mod.__captures__
      for var in captures_tuple:
        if not type(var) in var_types:
          continue
        current = _navigate_to_path(state, path)
        for key, value in var.items():
          current[key] = type(var)(value)
      delattr(mod, '__captures__')

