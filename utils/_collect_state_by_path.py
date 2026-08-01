
def _collect_state_by_path(state):
  """Build a mapping from module path to state Variables."""
  state_by_path = {}

  def collect(s, path_parts):
    if isinstance(s, MutableMapping):
      for key, value in s.items():
        if isinstance(value, variableslib.Variable):
          path_tuple = tuple(path_parts)
          if path_tuple not in state_by_path:
            state_by_path[path_tuple] = {}
          state_by_path[path_tuple][key] = value
        elif isinstance(value, MutableMapping):
          collect(value, path_parts + [key])

  collect(state, [])
  return state_by_path

