
def _aggregate_at_state(joint_policies, state, player):
  """Returns {action: prob} for `player` in `state` for all joint policies.

  Args:
    joint_policies: List of joint policies.
    state: Openspiel State
    player: Current Player

  Returns:
    {action: prob} for `player` in `state` for all joint policies.
  """
  return [
      joint_policy[player].action_probabilities(state, player_id=player)
      for joint_policy in joint_policies
  ]

