from typing import Dict, List

def _regret_matching(
    cumulative_regrets: Dict[int, float], legal_actions: List[int]
) -> Dict[int, float]:
  """Returns an info state policy by applying regret-matching.

  Args:
    cumulative_regrets: A {action: cumulative_regret} dictionary.
    legal_actions: the list of legal actions at this state.

  Returns:
    A dict of action -> prob for all legal actions.
  """
  regrets = cumulative_regrets.values()
  sum_positive_regrets = sum((regret for regret in regrets if regret > 0))

  info_state_policy = {}
  if sum_positive_regrets > 0:
    for action in legal_actions:
      positive_action_regret = max(0.0, cumulative_regrets[action])
      info_state_policy[action] = (
          positive_action_regret / sum_positive_regrets)
  else:
    for action in legal_actions:
      info_state_policy[action] = 1.0 / len(legal_actions)
  return info_state_policy

