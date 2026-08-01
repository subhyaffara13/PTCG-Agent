
def projected_replicator_dynamics(payoff_tensors,
                                  prd_initial_strategies=None,
                                  prd_iterations=int(1e5),
                                  prd_dt=1e-3,
                                  prd_gamma=1e-6,
                                  average_over_last_n_strategies=None,
                                  use_approx=False,
                                  **unused_kwargs):
  """The Projected Replicator Dynamics algorithm.

  Args:
    payoff_tensors: List of payoff tensors for each player.
    prd_initial_strategies: Initial list of the strategies used by each player,
      if any. Could be used to speed up the search by providing a good initial
      solution.
    prd_iterations: Number of algorithmic steps to take before returning an
      answer.
    prd_dt: Update amplitude term.
    prd_gamma: Minimum exploratory probability term.
    average_over_last_n_strategies: Running average window size for average
      policy computation. If None, use the whole trajectory.
    use_approx: use the approximate simplex projection.
    **unused_kwargs: Convenient way of exposing an API compatible with other
      methods with possibly different arguments.

  Returns:
    PRD-computed strategies.
  """
  number_players = len(payoff_tensors)
  # Number of actions available to each player.
  action_space_shapes = payoff_tensors[0].shape

  # If no initial starting position is given, start with uniform probabilities.
  new_strategies = prd_initial_strategies or [
      np.ones(action_space_shapes[k]) / action_space_shapes[k]
      for k in range(number_players)
  ]

  averager = nfg_utils.StrategyAverager(number_players, action_space_shapes,
                                        average_over_last_n_strategies)
  averager.append(new_strategies)

  for _ in range(prd_iterations):
    new_strategies = _projected_replicator_dynamics_step(
        payoff_tensors, new_strategies, prd_dt, prd_gamma, use_approx)
    averager.append(new_strategies)
  return averager.average_strategies()

