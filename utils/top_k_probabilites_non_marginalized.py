
def top_k_probabilites_non_marginalized(solver):
  """Returns [kwargs] policies with highest selection probabilities.

  Args:
    solver: A GenPSROSolver instance.
  """
  kwargs = solver.get_kwargs()
  # By default, select only 1 new policy to optimize from.
  number_policies_to_select = kwargs.get("number_policies_selected") or 1

  ids = solver.get_joint_policy_ids()

  effective_number = min(number_policies_to_select, len(ids))
  joint_strategy_probabilities = (
      solver.get_and_update_non_marginalized_meta_strategies(update=False))

  sorted_list = sorted(
      zip(joint_strategy_probabilities, ids),
      reverse=True,
      key=lambda pair: pair[0])
  selected_policy_ids = [id_selected for _, id_selected in sorted_list
                        ][:effective_number]

  used_policies = solver.get_joint_policies_from_id_list(selected_policy_ids)
  return used_policies, get_indices_from_non_marginalized(used_policies)

