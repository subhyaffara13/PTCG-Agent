
def exhaustive_non_marginalized(solver):
  """Returns every player's policies.

  Args:
    solver: A GenPSROSolver instance.
  """
  used_policies = solver.get_policies()
  return used_policies, get_indices_from_non_marginalized(used_policies)

