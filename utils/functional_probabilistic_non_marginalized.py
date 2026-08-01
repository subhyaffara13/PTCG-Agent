
def functional_probabilistic_non_marginalized(solver):
  """Returns [kwargs] randomly selected policies with generated probabilities.

  Args:
    solver: A GenPSROSolver instance.
  """
  kwargs = solver.get_kwargs()
  # By default, select only 1 new policy to optimize from.
  number_policies_to_select = kwargs.get("number_policies_selected") or 1
  # By default, use meta strategies.
  probability_computation_function = kwargs.get(
      "selection_probability_function") or compressed_lambda

  ids = solver.get_joint_policy_ids()
  joint_strategy_probabilities = probability_computation_function(solver)

  effective_number = min(number_policies_to_select, len(ids))
  selected_policies = list(
      np.random.choice(
          ids, effective_number, replace=False, p=joint_strategy_probabilities))
  used_policies = solver.get_joint_policies_from_id_list(selected_policies)
  return used_policies, get_indices_from_non_marginalized(used_policies)

