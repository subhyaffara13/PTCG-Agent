
def joint_action_probabilities_aux(state, policy):
  """Auxiliary function for joint_action_probabilities.

  Args:
    state: a game state at a simultaneous decision node.
    policy: policy that gives the probability distribution over the legal
      actions for each players.

  Returns:
    actions_per_player: list of list of actions for each player
    probs_per_player: list of list of probabilities do the corresponding action
     in actions_per_player for each player.
  """
  assert state.is_simultaneous_node()
  action_probs_per_player = [
      policy.action_probabilities(state, player)
      for player in range(state.get_game().num_players())
  ]
  actions_per_player = [pi.keys() for pi in action_probs_per_player]
  probs_per_player = [pi.values() for pi in action_probs_per_player]
  return actions_per_player, probs_per_player

