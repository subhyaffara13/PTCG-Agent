
def regret_matching(payoff_tensors,
                    initial_strategies=None,
                    iterations=int(1e5),
                    gamma=1e-6,
                    average_over_last_n_strategies=None,
                    **unused_kwargs):
  """Runs regret-matching for the stated number of iterations.

  Args:
    payoff_tensors: List of payoff tensors for each player.
    initial_strategies: Initial list of the strategies used by each player, if
      any. Could be used to speed up the search by providing a good initial
      solution.
    iterations: Number of algorithmic steps to take before returning an answer.
    gamma: Minimum exploratory probability term.
    average_over_last_n_strategies: Running average window size for average
      policy computation. If None, use the whole trajectory.
    **unused_kwargs: Convenient way of exposing an API compatible with other
      methods with possibly different arguments.

  Returns:
    RM-computed strategies.
  """
  number_players = len(payoff_tensors)
  # Number of actions available to each player.
  action_space_shapes = payoff_tensors[0].shape

  # If no initial starting position is given, start with uniform probabilities.
  new_strategies = initial_strategies or [
      np.ones(action_space_shapes[k]) / action_space_shapes[k]
      for k in range(number_players)
  ]

  regrets = [
      np.ones(action_space_shapes[k]) / INITIAL_REGRET_DENOM
      for k in range(number_players)
  ]

  averager = nfg_utils.StrategyAverager(number_players, action_space_shapes,
                                        average_over_last_n_strategies)
  averager.append(new_strategies)

  for _ in range(iterations):
    new_strategies = _regret_matching_step(payoff_tensors, new_strategies,
                                           regrets, gamma)
    averager.append(new_strategies)
  return averager.average_strategies()


def regret_matching(regrets):
  regrets = np.array(regrets)
  regret_plus = regrets * (regrets > 0.0)
  regrets_sum = np.sum(regret_plus, axis=-1)
  regret_plus[regrets_sum > 0.0, :] = regret_plus[
      regrets_sum > 0.0, :
  ] / regrets_sum[regrets_sum > 0.0].reshape(-1, 1)
  regret_plus[regrets_sum <= 0.0, :] = (
      np.ones_like(regret_plus[regrets_sum <= 0.0, :]) / regret_plus.shape[-1]
  )
  return regret_plus


def regret_matching(regret, mask):
  """Computes current policy based on current regrets.

  Args:
    regret: Current regrets in array Fkiat[Isets, Actions]
    mask: Legal action mask Bool[Isets, Actions]

  Returns:
    policy: the policy.
  """
  regret = jnp.maximum(regret, 0) * mask
  total = jnp.sum(regret, axis=-1, keepdims=True)

  return jnp.where(total > 0.0, regret / total, 1.0 / jnp.sum(mask)) * mask

