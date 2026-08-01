
def _project_distribution(updated_strategy, gamma):
  """Projects the distribution in updated_x to have minimal probabilities.

  Minimal probabilities are set as gamma, and the probabilities are then
  renormalized to sum to 1.

  Args:
    updated_strategy: New distribution value after being updated by update rule.
    gamma: minimal probability value when divided by number of actions.

  Returns:
    Projected distribution.
  """
  # Epsilon approximation of L2-norm projection onto the Delta_gamma space.
  updated_strategy[updated_strategy < gamma] = gamma
  updated_strategy = updated_strategy / np.sum(updated_strategy)
  return updated_strategy

