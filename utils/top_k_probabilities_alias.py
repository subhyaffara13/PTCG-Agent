
def top_k_probabilities_alias(solver, number_policies_to_select):
  """Returns [kwargs] policies with highest selection probabilities.

  Args:
    solver: A GenPSROSolver instance.
    number_policies_to_select: Number policies to select
  """
  policies = solver.get_policies()
  num_players = len(policies)
  meta_strategy_probabilities = solver.get_meta_strategies()

  used_policies = []
  used_policy_indexes = []
  for k in range(num_players):
    current_policies = policies[k]
    current_selection_probabilities = meta_strategy_probabilities[k]
    effective_number = min(number_policies_to_select, len(current_policies))

    # pylint: disable=g-complex-comprehension
    selected_indexes = [
        index for _, index in sorted(
            zip(current_selection_probabilities,
                list(range(len(current_policies)))),
            key=lambda pair: pair[0])
    ][:effective_number]

    selected_policies = [current_policies[i] for i in selected_indexes]
    used_policies.append(selected_policies)
    used_policy_indexes.append(selected_indexes)
  return used_policies, used_policy_indexes

