
def payoff_evaluation(
    cv_calc: coalitional_game.CoalitionalGame,
    payoffs: np.ndarray,
    epsilon: float,
    batch_size: int,
    max_exponent: int = 13,
) -> float:
  """Evaluate deficit over a set of random coalitions.

  Args:
    cv_calc: the game to work on
    payoffs: the payoff vector to test
    epsilon: desired approximation of the epsilon-core
    batch_size: number of random coalitions to sample
    max_exponent: examine at maxixum 2**max_exponent constraints in one batch
      default 13, assume 2**13 ~ 10k coalitions is mem limit for single batch

  Returns:
    Expected loss, relu(deficit), over random batch of coalitions
  """
  max_batch = 2**max_exponent
  num_players = cv_calc.num_players()
  violation = 0.
  if batch_size >= 2**num_players:
    num_suffix_repeats = min(max_exponent, num_players)
    num_prefix_repeats = max(0, num_players - num_suffix_repeats)
    zo = [0, 1]
    suffix = np.array(list(itertools.product(zo, repeat=num_suffix_repeats)))
    prefixes = itertools.product(zo, repeat=num_prefix_repeats)
    for prefix in prefixes:
      if prefix:
        prefix_rep = np.repeat([prefix], suffix.shape[0], axis=0)
        coalitions = np.concatenate([prefix_rep, suffix], axis=1)
      else:
        coalitions = suffix
      batch_contributions = cv_calc.coalition_values(coalitions)
      batch_payouts = np.dot(coalitions, payoffs)
      batch_deficits = batch_contributions - batch_payouts - epsilon
      batch_deficits = np.clip(batch_deficits, 0., np.inf)
      violation = max(violation, np.max(batch_deficits))
  else:
    q, r = divmod(batch_size, max_batch)
    num_loops = q + (r > 0)
    for _ in range(num_loops):
      coalitions = np.random.randint(2, size=(max_batch, num_players))
      batch_contributions = cv_calc.coalition_values(coalitions)
      batch_payouts = np.dot(coalitions, payoffs)
      batch_deficits = batch_contributions - batch_payouts - epsilon
      batch_deficits = np.clip(batch_deficits, 0., np.inf)
      violation = max(violation, np.max(batch_deficits))
  return float(violation)

