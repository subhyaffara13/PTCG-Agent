
def probabilistic_non_marginalized(solver):
  """Returns [kwargs] policies randomly, proportionally with selection probas.

  Args:
    solver: A GenPSROSolver instance.
  """
  kwargs = solver.get_kwargs()
  # By default, select only 1 new policy to optimize from.
  number_policies_to_select = kwargs.get("number_policies_selected") or 1

  # Get integer IDs and probabilities of meta-strategies
  ids = solver.get_joint_policy_ids()
  joint_strategy_probabilities = (
      solver.get_and_update_non_marginalized_meta_strategies(update=False))

  effective_number = min(number_policies_to_select, len(ids))
  selected_policy_ids = list(
      np.random.choice(
          ids, effective_number, replace=False, p=joint_strategy_probabilities))
  used_policies = solver.get_joint_policies_from_id_list(selected_policy_ids)
  return used_policies, get_indices_from_non_marginalized(used_policies)

