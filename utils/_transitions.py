
def _transitions(state, policies):
  """Returns a list of (action, prob) pairs from the specified state."""
  if state.is_chance_node():
    return state.chance_outcomes()
  else:
    pl = state.current_player()
    return list(policies[pl].action_probabilities(state).items())


def _transitions(state, policies):
  """Returns iterator over (action, prob) from the given state."""
  if state.is_chance_node():
    return state.chance_outcomes()
  elif state.is_simultaneous_node():
    return policy.joint_action_probabilities(state, policies)
  else:
    player = state.current_player()
    return policies[player].action_probabilities(state).items()

