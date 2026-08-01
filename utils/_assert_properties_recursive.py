
def _assert_properties_recursive(state, assert_functions):

  for assert_function in assert_functions:
    assert_function(state)

  # Recursion
  # TODO(author2): We often use a `give me the next node` function and we
  # probably want a utility method for that, which works for all games.
  if state.is_terminal():
    return
  elif state.is_chance_node():
    for action, unused_prob in state.chance_outcomes():
      state_for_search = state.child(action)
      _assert_properties_recursive(state_for_search, assert_functions)
  else:
    for action in state.legal_actions():
      state_for_search = state.child(action)
      _assert_properties_recursive(state_for_search, assert_functions)

