
def current_path():
  """Current state_dict path during deserialization for error messages."""
  return '/'.join(_error_context.path)

