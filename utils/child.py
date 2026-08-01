
def child(state, action):
  """Returns a child state, handling the simultaneous node case."""
  if isinstance(action, Iterable):
    child_state = state.clone()
    child_state.apply_actions(action)
    return child_state
  else:
    return state.child(action)

