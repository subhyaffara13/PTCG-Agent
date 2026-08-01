
def get_alpharank_marginals(payoff_tables, pi):
  """Returns marginal strategy rankings for each player given joint rankings pi.

  Args:
    payoff_tables: List of meta-game payoff tables for a K-player game, where
      each table has dim [n_strategies_player_1 x ... x n_strategies_player_K].
      These payoff tables may be asymmetric.
    pi: The vector of joint rankings as computed by alpharank. Each element i
      corresponds to a unique integer ID representing a given strategy profile,
      with profile_to_id mappings provided by
      alpharank_utils.get_id_from_strat_profile().

  Returns:
    pi_marginals: List of np.arrays of player-wise marginal strategy masses,
      where the k-th player's np.array has shape [n_strategies_player_k].
  """
  num_populations = len(payoff_tables)

  if num_populations == 1:
    return pi
  else:
    num_strats_per_population = alpharank_utils.get_num_strats_per_population(
        payoff_tables, payoffs_are_hpt_format=False)
    num_profiles = alpharank_utils.get_num_profiles(num_strats_per_population)
    pi_marginals = [np.zeros(n) for n in num_strats_per_population]
    for i_strat in range(num_profiles):
      strat_profile = (
          alpharank_utils.get_strat_profile_from_id(num_strats_per_population,
                                                    i_strat))
      for i_player in range(num_populations):
        pi_marginals[i_player][strat_profile[i_player]] += pi[i_strat]
    return pi_marginals

