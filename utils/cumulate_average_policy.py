
def cumulate_average_policy(infostates: List[InfostateNode],
                            weight: int = 1) -> None:
  """Cumulates policy values of each infostate in infostates.

  For each infostate, we update average policy and the sum of weighted average
  policy.

  Args:
    infostates: List of information states.
    weight: The weight we use to update policy and sum of weighted average
      policy. For CFR algorithm, weight is 1.
  """
  for infostate in infostates:
    for action in infostate.get_actions():
      infostate.average_policy[
          action] += infostate.player_reach_prob * infostate.policy[
              action] * weight
    infostate.average_policy_weight_sum += infostate.player_reach_prob * weight

