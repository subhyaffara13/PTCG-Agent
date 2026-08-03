from typing import List

def update_regrets(regret):
  """Updates the regrets without CFRPlus."""
  return regret


def update_regrets(infostates: List[InfostateNode]) -> None:
  """Updates regret value for each infostate in infostates.

  Args:
    infostates: List of information states
  """
  for infostate in infostates:
    for action in infostate.get_actions():
      current_regret = infostate.counterfactual_action_values[
          action] - infostate.counterfactual_value
      infostate.regret[action] += current_regret

