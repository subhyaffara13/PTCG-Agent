
def get_num_profiles(num_strats_per_population):
  """Returns the total number of pure strategy profiles.

  Args:
    num_strats_per_population: A list of size `num_populations` of the number of
      strategies per population.

  Returns:
    The total number of pure strategy profiles.
  """
  return np.prod(num_strats_per_population)

