
def _regret_matching_step(payoff_tensors, strategies, regrets, gamma):
  """Does one step of the projected replicator dynamics algorithm.

  Args:
    payoff_tensors: List of payoff tensors for each player.
    strategies: List of the strategies used by each player.
    regrets: List of cumulative regrets used by each player.
    gamma: Minimum exploratory probability term.

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
    regrets[player] += values_per_strategy - average_return

    updated_strategy = regrets[player].copy()
    updated_strategy[updated_strategy < 0] = 0.0
    sum_regret = updated_strategy.sum()
    uniform_strategy = np.ones(len(updated_strategy)) / len(updated_strategy)

    if sum_regret > 0:
      updated_strategy /= sum_regret
      updated_strategy = gamma * uniform_strategy + (1 -
                                                     gamma) * updated_strategy
    else:
      updated_strategy = uniform_strategy

    new_strategies.append(updated_strategy)
  return new_strategies

