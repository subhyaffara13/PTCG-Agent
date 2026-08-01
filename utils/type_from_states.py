
def type_from_states(states):
  """Get node type of a list of states and assert they are the same."""
  types = [state.get_type() for state in states]
  assert len(set(types)) == 1
  return types[0]


def type_from_states(states):
  """Get node type of a list of states and assert they are the same."""
  types = [state.get_type() for state in states]
  assert len(set(types)) == 1, f"types: {types}"
  return types[0]

