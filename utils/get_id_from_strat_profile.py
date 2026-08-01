
def get_id_from_strat_profile(num_strats_per_population, strat_profile):
  """Returns a unique integer ID representing the requested strategy profile.

  Map any `strat_profile` (there are `np.prod(num_strats_per_population)` such
  profiles) to {0,..., num_strat_profiles - 1}.

  The mapping is done using a usual counting strategy: With
  num_strats_per_population = [a1, ..., a_n]
  strat_profile = [b1, ..., b_n]

  we have

  id = b_1 + a1 * (b2 + a_2 * (b3 + a_3 *...))


  This is helpful for querying the element of our finite-population Markov
  transition matrix that corresponds to a transition between a specific pair of
  strategy profiles.

  Args:
    num_strats_per_population: List of strategy sizes for each population.
    strat_profile: The strategy profile (list of integers corresponding to the
      strategy of each agent) whose ID is requested.

  Returns:
    Unique ID of strat_profile.
  """

  if len(strat_profile) == 1:
    return strat_profile[0]

  return strat_profile[-1] + (num_strats_per_population[-1] *
                              get_id_from_strat_profile(
                                  num_strats_per_population[:-1],
                                  strat_profile[:-1]))

