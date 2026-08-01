
def probabilistic_alias(solver, number_policies_to_select):
  """Returns [kwargs] policies randomly, proportionally with selection probas.

  Args:
    solver: A GenPSROSolver instance.
    number_policies_to_select: Number policies to select
  """
  policies = solver.get_policies()
  num_players = len(policies)
  meta_strategy_probabilities = solver.get_meta_strategies()

  print(policies, meta_strategy_probabilities)
  used_policies = []
  used_policy_indexes = []
  for k in range(num_players):
    current_policies = policies[k]
    current_selection_probabilities = meta_strategy_probabilities[k]
    effective_number = min(number_policies_to_select, len(current_policies))

    selected_indexes = list(
        np.random.choice(
            list(range(len(current_policies))),
            effective_number,
            replace=False,
            p=current_selection_probabilities))
    selected_policies = [current_policies[i] for i in selected_indexes]
    used_policies.append(selected_policies)
    used_policy_indexes.append(selected_indexes)
  return used_policies, used_policy_indexes

