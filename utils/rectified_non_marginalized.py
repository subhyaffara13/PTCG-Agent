
def rectified_non_marginalized(solver):
  """Returns every strategy with nonzero selection probability.

  Args:
    solver: A GenPSROSolver instance.
  """
  used_policies = []
  policies = solver.get_policies()
  num_players = len(policies)
  meta_strategy_probabilities = (
      solver.get_and_update_non_marginalized_meta_strategies(update=False))
  for k in range(num_players):
    current_policies = policies[k]
    current_probabilities = meta_strategy_probabilities[k]
    current_policies = [
        current_policies[i]
        for i in range(len(current_policies))
        if current_probabilities[i] > EPSILON_MIN_POSITIVE_PROBA
    ]
    used_policies.append(current_policies)
  return used_policies, get_indices_from_non_marginalized(used_policies)

