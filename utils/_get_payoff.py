
def _get_payoff(payoff_table_k, payoffs_are_hpt_format, strat_profile, k=None):
  """Gets the payoff of the k-th agent in a single or multi-population game.

  Namely, accepts the payoff table of the k-th agent (which can be matrix or
  HPT format), the index k of the agent of interest (so its payoff can be looked
  up in case of an HPT format payoff table), and the pure strategy profile.

  For multipopulation games, we currently only support games where the k-th
  agent's payoff is a function of the HPT distribution (a vector
  indicating the number of players playing each strategy), as opposed to the
  strategy profile (a vector indicating the strategy of each player). This is
  due to the nature of the PayoffTable class, which currently only tracks
  distributions in the first k columns (rather than profiles).

  Args:
    payoff_table_k: The k-th agent's payoff table, in matrix or HPT format.
    payoffs_are_hpt_format: Boolean indicating whether payoff_table_k is a
      _PayoffTableInterface object (AKA Heuristic Payoff Table or HPT) or a
      numpy array. True indicates HPT format, False indicates numpy array.
    strat_profile: The pure strategy profile.
    k: The index of the agent of interest. Only used for HPT case, and only >0
      for a multi-population game.

  Returns:
    The k-th agent's payoff.
  """

  if payoffs_are_hpt_format:
    # All games are supported when using HPTs
    if k is None:
      raise ValueError('Agent index k must be provided for HPT format payoffs')

    # Compute HPT distribution (vector of # of players per strategy)
    distribution = payoff_table_k.get_distribution_from_profile(strat_profile)
    # Lookup the payoff profile (HPT row) corresponding to the distribution
    payoff_profile = payoff_table_k[tuple(distribution)]
    # Return the payoff corresponding to the k-th agent's strategy
    return payoff_profile[strat_profile[k]]
  else:
    # Only 2 player symmetric/asymmetric games supported using matrix payoffs
    return payoff_table_k[tuple(strat_profile)]

