
def nash_strategy(solver, return_joint=False):
  """Returns nash distribution on meta game matrix.

  This method only works for two player zero-sum games.

  Args:
    solver: GenPSROSolver instance.
    return_joint: If true, only returns marginals. Otherwise marginals as well
      as joint probabilities.

  Returns:
    Nash distribution on strategies.
  """
  meta_games = solver.get_meta_game()
  if not isinstance(meta_games, list):
    meta_games = [meta_games, -meta_games]
  meta_games = [x.tolist() for x in meta_games]
  if len(meta_games) != 2:
    raise NotImplementedError(
        "nash_strategy solver works only for 2p zero-sum"
        "games, but was invoked for a {} player game".format(len(meta_games)))
  nash_prob_1, nash_prob_2, _, _ = (
      lp_solver.solve_zero_sum_matrix_game(
          pyspiel.create_matrix_game(*meta_games)))
  result = [
      renormalize(np.array(nash_prob_1).reshape(-1)),
      renormalize(np.array(nash_prob_2).reshape(-1))
  ]

  if not return_joint:
    return result
  else:
    joint_strategies = get_joint_strategy_from_marginals(result)
    return result, joint_strategies

