
def _initialize_maps(states, values, transitions):
  """Initialize the value and transition maps."""
  for key, state in states.items():
    if state.is_terminal():
      values[key] = state.player_return(0)
    else:
      values[key] = 0
      _add_transition(transitions, key, state)

