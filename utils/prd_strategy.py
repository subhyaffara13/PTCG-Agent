
def prd_strategy(solver, return_joint=False):
  """Computes Projected Replicator Dynamics strategies.

  Args:
    solver: GenPSROSolver instance.
    return_joint: If true, only returns marginals. Otherwise marginals as well
      as joint probabilities.

  Returns:
    PRD-computed strategies.
  """
  meta_games = solver.get_meta_game()
  if not isinstance(meta_games, list):
    meta_games = [meta_games, -meta_games]
  kwargs = solver.get_kwargs()
  result = projected_replicator_dynamics.projected_replicator_dynamics(
      meta_games, **kwargs)
  if not return_joint:
    return result
  else:
    joint_strategies = get_joint_strategy_from_marginals(result)
    return result, joint_strategies

