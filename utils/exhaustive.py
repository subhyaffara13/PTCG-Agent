
def exhaustive(solver, number_policies_selected=1):
  """Returns every player's policies.

  Args:
    solver: A GenPSROSolver instance.
    number_policies_selected: Number of policies to return for each player.
      (Compatibility argument)

  Returns:
    used_policies : List of size 'num_players' of lists of size
      min('number_policies_selected', num_policies') containing selected
      policies.
    used_policies_indexes: List of lists of the same shape as used_policies,
      containing the list indexes of selected policies.
  """
  del number_policies_selected
  policies = solver.get_policies()
  indexes = [list(range(len(pol))) for pol in policies]
  return policies, indexes

