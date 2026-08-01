
def _add_transition(transitions, key, state):
  """Adds action transitions from given state."""

  if state.is_simultaneous_node():
    for p0action in state.legal_actions(0):
      for p1action in state.legal_actions(1):
        next_state = state.clone()
        next_state.apply_actions([p0action, p1action])
        possibilities = []
        _get_future_states(possibilities, next_state)
        transitions[(key, p0action, p1action)] = possibilities
  else:
    for action in state.legal_actions():
      next_state = state.child(action)
      possibilities = []
      _get_future_states(possibilities, next_state)
      transitions[(key, action)] = possibilities

