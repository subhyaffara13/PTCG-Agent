
def alpharank_strategy(solver, return_joint=False, **unused_kwargs):
  """Returns AlphaRank distribution on meta game matrix.

  This method works for general games.

  Args:
    solver: GenPSROSolver instance.
    return_joint: a boolean specifying whether to return player-wise
      marginals.

  Returns:
    marginals: a list, specifying for each player the alpharank marginal
      distributions on their strategies.
    joint_distr: a list, specifying the joint alpharank distributions for all
      strategy profiles.
  """
  meta_games = solver.get_meta_game()
  meta_games = [np.asarray(x) for x in meta_games]

  if solver.symmetric_game:
    meta_games = [meta_games[0]]

    # Get alpharank distribution via alpha-sweep
    joint_distr = alpharank.sweep_pi_vs_epsilon(
        meta_games)
    joint_distr = remove_epsilon_negative_probs(joint_distr)

    marginals = 2 * [joint_distr]
    joint_distr = get_joint_strategy_from_marginals(marginals)
    if return_joint:
      return marginals, joint_distr
    else:
      return joint_distr

  else:
    joint_distr = alpharank.sweep_pi_vs_epsilon(meta_games)
    joint_distr = remove_epsilon_negative_probs(joint_distr)

    if return_joint:
      marginals = get_alpharank_marginals(meta_games, joint_distr)
      return marginals, joint_distr
    else:
      return joint_distr

