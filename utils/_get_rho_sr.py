
def _get_rho_sr(payoff_table,
                payoffs_are_hpt_format,
                m,
                r,
                s,
                alpha,
                game_is_constant_sum,
                use_local_selection_model,
                payoff_sum=None):
  """Gets fixation probability of rogue strategy r in population playing s.

  Args:
    payoff_table: A payoff table.
    payoffs_are_hpt_format: Boolean indicating whether payoff_table is a
      _PayoffTableInterface object (AKA Heuristic Payoff Table or HPT), or a
      numpy array. True indicates HPT format, False indicates numpy array.
    m: The total number of agents in the population.
    r: Rogue strategy r.
    s: Population strategy s.
    alpha: Fermi distribution temperature parameter.
    game_is_constant_sum: Boolean indicating if the game is constant sum.
    use_local_selection_model: Enable local evolutionary selection model, which
      considers fitness against the current opponent only, rather than the
      global population state.
    payoff_sum: The payoff sum if the game is constant sum, or None otherwise.

  Returns:
    The fixation probability.
  """

  if use_local_selection_model or game_is_constant_sum:
    payoff_rs = _get_payoff(
        payoff_table, payoffs_are_hpt_format, strat_profile=[r, s], k=0)
    if use_local_selection_model:
      # Row plays s, column plays r
      payoff_sr = _get_payoff(
          payoff_table, payoffs_are_hpt_format, strat_profile=[s, r], k=0)
      u = alpha * (payoff_rs - payoff_sr)
    else:
      if payoff_sum is None:
        raise ValueError(
            'payoff_sum must not be None for multi-population games'
        )
      u = alpha * m / (m - 1) * (payoff_rs - payoff_sum / 2)

    if np.isclose(u, 0, atol=1e-14):
      # To avoid divide by 0, use first-order approximation when u is near 0
      result = 1 / m
    else:
      result = (1 - np.exp(-u)) / (1 - np.exp(-m * u))
  else:
    if payoff_sum is not None:
      raise ValueError('payoff_sum must be None for single-population games')
    summed = 0
    for l in range(1, m):
      t_mult = 1.
      for p_r in range(1, l + 1):
        # Probabilities of strategy r decreasing/increasing
        p_s = m - p_r
        # Fitness of agent playing r against rest of current population
        f_ri = _get_singlepop_2player_fitness(
            payoff_table,
            payoffs_are_hpt_format,
            m,
            my_popsize=p_r,
            my_strat=r,
            opponent_strat=s,
            use_local_selection_model=use_local_selection_model)
        # Fitness of agent playing s against rest of current population
        f_sj = _get_singlepop_2player_fitness(
            payoff_table,
            payoffs_are_hpt_format,
            m,
            my_popsize=p_s,
            my_strat=s,
            opponent_strat=r,
            use_local_selection_model=use_local_selection_model)
        t_mult *= np.exp(-alpha * (f_ri - f_sj))
      summed += t_mult
    result = (1 + summed)**(-1)
  return result

