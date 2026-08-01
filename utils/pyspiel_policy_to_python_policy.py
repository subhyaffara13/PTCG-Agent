
def pyspiel_policy_to_python_policy(game, pyspiel_tabular_policy, players=None):
  """Converts a pyspiel.TabularPolicy to a TabularPolicy.

  Args:
    game: The OpenSpiel game.
    pyspiel_tabular_policy: Pyspiel tabular policy to copy from.
    players: List of integer player ids to copy policy from. For example,
      `players=[0]` will only copy player 0's policy over into the python policy
      (the other player's policies will be undefined). Default value of `None`
      will copy all players' policies.

  Returns:
    python_policy
  """
  policy = TabularPolicy(game, players=players)
  for item in pyspiel_tabular_policy.policy_table().items():
    info_state_str, actions_probs = item
    # If requested, only populate a policy for particular players.
    if players is not None and info_state_str not in policy.state_lookup:
      continue
    state_policy = policy.policy_for_key(info_state_str)
    if actions_probs:
      state_policy[:] = 0.0  # Ensure policy is zero by default.
    for action, prob in actions_probs:
      state_policy[action] = prob
  return policy

