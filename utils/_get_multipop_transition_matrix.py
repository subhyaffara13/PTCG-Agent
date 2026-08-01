
def _get_multipop_transition_matrix(payoff_tables,
                                    payoffs_are_hpt_format,
                                    m,
                                    alpha,
                                    use_inf_alpha=False,
                                    inf_alpha_eps=0.1):
  """Gets Markov transition matrix for multipopulation games."""

  num_strats_per_population = utils.get_num_strats_per_population(
      payoff_tables, payoffs_are_hpt_format)
  num_profiles = utils.get_num_profiles(num_strats_per_population)

  eta = 1. / (np.sum(num_strats_per_population - 1))

  c = np.zeros((num_profiles, num_profiles))
  rhos = np.zeros((num_profiles, num_profiles))

  for id_row_profile in range(num_profiles):
    row_profile = utils.get_strat_profile_from_id(num_strats_per_population,
                                                  id_row_profile)

    next_profile_gen = utils.get_valid_next_profiles(num_strats_per_population,
                                                     row_profile)

    for index_population_that_changed, col_profile in next_profile_gen:
      id_col_profile = utils.get_id_from_strat_profile(
          num_strats_per_population, col_profile)
      if use_inf_alpha:
        payoff_col = _get_payoff(
            payoff_tables[index_population_that_changed],
            payoffs_are_hpt_format,
            col_profile,
            k=index_population_that_changed)
        payoff_row = _get_payoff(
            payoff_tables[index_population_that_changed],
            payoffs_are_hpt_format,
            row_profile,
            k=index_population_that_changed)
        if np.isclose(payoff_col, payoff_row, atol=1e-14):
          c[id_row_profile, id_col_profile] = eta * 0.5
        elif payoff_col > payoff_row:
          # Transition to col strategy since its payoff is higher than row
          # strategy, but remove some small amount of mass, inf_alpha_eps, to
          # keep the chain irreducible
          c[id_row_profile, id_col_profile] = eta * (1 - inf_alpha_eps)
        else:
          # Transition with very small probability
          c[id_row_profile, id_col_profile] = eta * inf_alpha_eps
      else:
        rhos[id_row_profile, id_col_profile] = _get_rho_sr_multipop(
            payoff_table_k=payoff_tables[index_population_that_changed],
            payoffs_are_hpt_format=payoffs_are_hpt_format,
            k=index_population_that_changed,
            m=m,
            r=col_profile,
            s=row_profile,
            alpha=alpha)
        c[id_row_profile,
          id_col_profile] = eta * rhos[id_row_profile, id_col_profile]
    # Special case of self-transition
    c[id_row_profile, id_row_profile] = 1 - sum(c[id_row_profile, :])

  return c, rhos

