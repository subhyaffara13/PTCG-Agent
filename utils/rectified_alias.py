
def rectified_alias(solver, number_policies_to_select):
  """Returns every strategy with nonzero selection probability.

  Args:
    solver: A GenPSROSolver instance.
    number_policies_to_select: Number policies to select

  Returns:
    used_policies: A list, each element a list of the policies used per player.
  """
  del number_policies_to_select

  used_policies = []
  used_policy_indexes = []

  policies = solver.get_policies()
  num_players = len(policies)
  meta_strategy_probabilities = solver.get_meta_strategies()

  for k in range(num_players):
    current_policies = policies[k]
    current_probabilities = meta_strategy_probabilities[k]

    current_indexes = [
        i for i in range(len(current_policies))
        if current_probabilities[i] > EPSILON_MIN_POSITIVE_PROBA
    ]
    current_policies = [
        current_policies[i]
        for i in current_indexes
    ]

    used_policy_indexes.append(current_indexes)
    used_policies.append(current_policies)
  return used_policies, used_policy_indexes

