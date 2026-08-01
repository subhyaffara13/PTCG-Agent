
def _get_singlepop_transition_matrix(payoff_table,
                                     payoffs_are_hpt_format,
                                     m,
                                     alpha,
                                     game_is_constant_sum,
                                     use_local_selection_model,
                                     payoff_sum,
                                     use_inf_alpha=False,
                                     inf_alpha_eps=0.1):
  """Gets the Markov transition matrix for a single-population game.

  Args:
    payoff_table: A payoff table.
    payoffs_are_hpt_format: Boolean indicating whether payoff_table is a
      _PayoffTableInterface object (AKA Heuristic Payoff Table or HPT), or a
      numpy array. True indicates HPT format, False indicates numpy array.
    m: Total number of agents in the k-th population.
    alpha: Fermi distribution temperature parameter.
    game_is_constant_sum: Boolean indicating if the game is constant sum.
    use_local_selection_model: Enable local evolutionary selection model, which
      considers fitness against the current opponent only, rather than the
      global population state.
    payoff_sum: The payoff sum if the game is constant sum, or None otherwise.
    use_inf_alpha: Use infinite-alpha alpharank model.
    inf_alpha_eps: Noise term (epsilon) used in infinite-alpha alpharank model.

  Returns:
    Markov transition matrix.
  """

  num_strats_per_population = utils.get_num_strats_per_population(
      [payoff_table], payoffs_are_hpt_format)
  num_strats = num_strats_per_population[0]

  c = np.zeros((num_strats, num_strats))
  rhos = np.zeros((num_strats, num_strats))

  # r and s are, respectively, the column and row strategy profiles
  for s in range(num_strats):  # Current strategy
    for r in range(num_strats):  # Next strategy
      if s != r:  # Compute off-diagonal fixation probabilities
        if use_inf_alpha:
          eta = 1. / (num_strats - 1)
          # Payoff of r when played against s
          payoff_rs = _get_payoff(
              payoff_table, payoffs_are_hpt_format, strat_profile=[r, s], k=0)
          # Payoff of s when played against r
          payoff_sr = _get_payoff(
              payoff_table, payoffs_are_hpt_format, strat_profile=[s, r], k=0)
          if np.isclose(payoff_rs, payoff_sr, atol=1e-14):
            c[s, r] = eta * 0.5
          elif payoff_rs > payoff_sr:
            # Transition to r since its payoff is higher than s, but remove some
            # small amount of mass, inf_alpha_eps, to keep the chain irreducible
            c[s, r] = eta * (1 - inf_alpha_eps)
          else:
            # Transition with very small probability
            c[s, r] = eta * inf_alpha_eps
        else:
          rhos[s, r] = _get_rho_sr(payoff_table, payoffs_are_hpt_format, m, r,
                                   s, alpha, game_is_constant_sum,
                                   use_local_selection_model, payoff_sum)
          eta = 1. / (num_strats - 1)
          c[s, r] = eta * rhos[s, r]
    # Fixation probability of competing only against one's own strategy is 1
    # rhos[s,s] = 1. # Commented as self-fixations are not interesting (for now)
    c[s, s] = 1 - sum(c[s, :])  # Diagonals

  return c, rhos

