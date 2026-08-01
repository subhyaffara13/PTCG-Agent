
def _navigate_to_path(state, path):
  """Navigate to a nested path in state, creating dicts as needed."""
  current = state
  for part in path:
    if part not in current:
      current[part] = State({})
    current = current[part]
  return current

