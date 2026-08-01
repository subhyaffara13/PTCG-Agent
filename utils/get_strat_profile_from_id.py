
def get_strat_profile_from_id(num_strats_per_population, profile_id):
  """Returns the strategy profile corresponding to a requested strategy ID.

  This is the inverse of the function get_id_from_strat_profile(). See that
  function for the indexing mechanism.

  Args:
    num_strats_per_population: List of strategy sizes for each population.
    profile_id: Integer ID of desired strategy profile, in
      {0,...,get_num_profiles-1}.

  Returns:
    The strategy profile whose ID was looked up.
  """

  num_populations = len(num_strats_per_population)
  strat_profile = np.zeros(num_populations, dtype=np.int32)

  for i_population in range(num_populations - 1, -1, -1):
    strat_profile[i_population] = (
        profile_id % num_strats_per_population[i_population])
    profile_id = profile_id // num_strats_per_population[i_population]

  return strat_profile

