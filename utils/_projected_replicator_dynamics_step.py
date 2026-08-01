
def _projected_replicator_dynamics_step(payoff_tensors, strategies, dt, gamma,
                                        use_approx=False):
  """Does one step of the projected replicator dynamics algorithm.

  Args:
    payoff_tensors: List of payoff tensors for each player.
    strategies: List of the strategies used by each player.
    dt: Update amplitude term.
    gamma: Minimum exploratory probability term.
    use_approx: use approximate simplex projection.

  Returns:
    A list of updated strategies for each player.
  """

  # TODO(author4): Investigate whether this update could be fully vectorized.
  new_strategies = []
  for player in range(len(payoff_tensors)):
    current_payoff_tensor = payoff_tensors[player]
    current_strategy = strategies[player]

    values_per_strategy = _partial_multi_dot(current_payoff_tensor, strategies,
                                             player)
    average_return = np.dot(values_per_strategy, current_strategy)
    delta = current_strategy * (values_per_strategy - average_return)

    updated_strategy = current_strategy + dt * delta
    updated_strategy = (
        _approx_simplex_projection(updated_strategy, gamma) if use_approx
        else _simplex_projection(updated_strategy, gamma))
    new_strategies.append(updated_strategy)
  return new_strategies

