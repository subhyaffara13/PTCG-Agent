
def get_valid_next_profiles(num_strats_per_population, cur_profile):
  """Generates monomorphic strategy profile transitions given cur_profile.

  Given a current strategy profile, cur_profile, this generates all follow-up
  profiles that involve only a single other population changing its current
  monomorphic strategy to some other monomorphic strategy. Note that
  self-transitions from cur_profile to cur_profile are not included here, as
  they are a special case in our Markov chain.

  Args:
    num_strats_per_population: List of strategy sizes for each population.
    cur_profile: Current strategy profile.

  Yields:
    The next valid strategy profile transition.
  """
  num_populations = len(num_strats_per_population)

  for i_population_to_change in range(num_populations):
    for new_strat in range(num_strats_per_population[i_population_to_change]):
      # Ensure a transition will actually happen
      if new_strat != cur_profile[i_population_to_change]:
        next_profile = cur_profile.copy()
        next_profile[i_population_to_change] = new_strat
        yield i_population_to_change, next_profile

