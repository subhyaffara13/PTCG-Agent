
def _next_states(states, to_string):
  next_states = {}
  for state in states:
    _get_next_states(state, next_states, to_string)
  return set(next_states.keys()), set(next_states.values())

