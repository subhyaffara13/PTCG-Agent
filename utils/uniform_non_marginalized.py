
def uniform_non_marginalized(solver):
  """Returns [kwargs] randomly selected policies (Uniform probability).

  Args:
    solver: A GenPSROSolver instance.
  """
  kwargs = solver.get_kwargs()
  # By default, select only 1 new policy to optimize from.
  number_policies_to_select = kwargs.get("number_policies_selected") or 1

  ids = solver.get_joint_policy_ids()

  effective_number = min(number_policies_to_select, len(ids))
  selected_policy_ids = list(
      np.random.choice(
          ids, effective_number, replace=False, p=np.ones(len(ids)) / len(ids)))
  used_policies = solver.get_joint_policies_from_id_list(selected_policy_ids)
  return used_policies, get_indices_from_non_marginalized(used_policies)

