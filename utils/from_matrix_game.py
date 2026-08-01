
def from_matrix_game(matrix_game):
  """Returns a PayOffTable given a symmetric 2-player matrix game.

  Args:
    matrix_game: The payoff matrix corresponding to a 2-player symmetric game.
  """

  if not isinstance(matrix_game, np.ndarray):
    raise ValueError("The matrix game should be a numpy array, not a {}".format(
        type(matrix_game)))
  num_strats_per_population = (
      utils.get_num_strats_per_population(
          payoff_tables=[matrix_game], payoffs_are_hpt_format=False))
  assert len(num_strats_per_population) == 2
  assert num_strats_per_population[0] == num_strats_per_population[1]
  num_strategies = num_strats_per_population[0]

  num_profiles = utils.get_num_profiles(num_strats_per_population)
  table = PayoffTable(num_players=2, num_strategies=num_strategies)

  # Construct the HPT by filling in the corresponding payoffs for each profile
  for id_profile in range(num_profiles):
    strat_profile = utils.get_strat_profile_from_id(num_strats_per_population,
                                                    id_profile)
    distribution = table.get_distribution_from_profile(strat_profile)
    # For symmetric matrix games, multiple strategy profiles correspond to the
    # same distribution and payoffs. Thus, ensure the table entry has not
    # already been filled by a previous strategy profile.
    if table.item_is_uninitialized(tuple(distribution)):
      payoffs = np.zeros(num_strategies)
      payoffs[strat_profile[0]] = matrix_game[strat_profile[0],
                                              strat_profile[1]]
      payoffs[strat_profile[1]] = matrix_game[strat_profile[1],
                                              strat_profile[0]]
      table[tuple(distribution)] = payoffs

  return table

