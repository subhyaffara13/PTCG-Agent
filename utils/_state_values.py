
def _state_values(state, num_players, policy):
  """Value of a state for every player given a policy."""
  if state.is_terminal():
    return np.array(state.returns())
  else:
    if state.is_simultaneous_node():
      p_action = tuple(policy_lib.joint_action_probabilities(state, policy))

    else:
      p_action = (
          state.chance_outcomes()
          if state.is_chance_node()
          else policy.action_probabilities(state).items()
      )
    return sum(
        prob
        * _state_values(policy_lib.child(state, action), num_players, policy)
        for action, prob in p_action
    )

