
def compute(payoff_tables,
            m=50,
            alpha=100,
            use_local_selection_model=True,
            verbose=False,
            use_inf_alpha=False,
            inf_alpha_eps=0.01):
  """Computes the finite population stationary statistics.

  Args:
    payoff_tables: List of game payoff tables, one for each agent identity. Each
      payoff_table may be either a numpy array, or a _PayoffTableInterface
      object.
    m: Finite population size.
    alpha: Fermi distribution temperature parameter.
    use_local_selection_model: Enable local evolutionary selection model, which
      considers fitness against the current opponent only, rather than the
      global population state.
    verbose: Set to True to print intermediate results.
    use_inf_alpha: Use infinite-alpha alpharank model.
    inf_alpha_eps: Noise term to use in infinite-alpha alpharank model.

  Returns:
    rhos: Matrix of strategy-to-strategy fixation probabilities.
    rho_m: Neutral fixation probability.
    pi: Finite population stationary distribution.
    num_strats: Number of available strategies.
  """
  payoffs_are_hpt_format = utils.check_payoffs_are_hpt(payoff_tables)

  num_populations = len(payoff_tables)

  num_strats_per_population = utils.get_num_strats_per_population(
      payoff_tables, payoffs_are_hpt_format)

  # Handles the trivial case of Markov chain with one state
  if np.array_equal(num_strats_per_population,
                    np.ones(len(num_strats_per_population))):
    rhos = np.asarray([[1]])
    rho_m = 1. / m if not use_inf_alpha else 1
    num_profiles = 1
    pi = np.asarray([1.])
    return rhos, rho_m, pi, num_profiles, num_strats_per_population

  if verbose:
    print('Constructing c matrix')
    print('num_strats_per_population:', num_strats_per_population)

  if num_populations == 1:
    # User fast closed-form analysis for constant-sum single-population games
    game_is_constant_sum, payoff_sum = utils.check_is_constant_sum(
        payoff_tables[0], payoffs_are_hpt_format)
    if verbose:
      print('game_is_constant_sum:', game_is_constant_sum, 'payoff sum: ',
            payoff_sum)
    # Single-population/symmetric game just uses the first player's payoffs
    c, rhos = _get_singlepop_transition_matrix(
        payoff_tables[0],
        payoffs_are_hpt_format,
        m,
        alpha,
        game_is_constant_sum,
        use_local_selection_model,
        payoff_sum,
        use_inf_alpha=use_inf_alpha,
        inf_alpha_eps=inf_alpha_eps)
    num_profiles = num_strats_per_population[0]
  else:
    c, rhos = _get_multipop_transition_matrix(
        payoff_tables,
        payoffs_are_hpt_format,
        m,
        alpha,
        use_inf_alpha=use_inf_alpha,
        inf_alpha_eps=inf_alpha_eps)
    num_profiles = utils.get_num_profiles(num_strats_per_population)

  pi = _get_stationary_distr(c)

  rho_m = 1. / m if not use_inf_alpha else 1  # Neutral fixation probability
  if verbose:
    print_results(payoff_tables, payoffs_are_hpt_format, rhos, rho_m, c, pi)

  return rhos, rho_m, pi, num_profiles, num_strats_per_population

