
def normalize_average_policy(infostates) -> None:
  """Updates infostate policy by normalizing average policy.

  Args:
    infostates: List of information states that their policies will be updated.
  """
  for infostate in infostates:
    for action in infostate.get_actions():
      infostate.policy[action] = infostate.average_policy[
          action] / infostate.average_policy_weight_sum

