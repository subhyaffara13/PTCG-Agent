
def get_strategy_profile_ids(payoff_tables):
  num_strats_per_population = (
      alpharank_utils.get_num_strats_per_population(
          payoff_tables, payoffs_are_hpt_format=False))
  return range(alpharank_utils.get_num_profiles(num_strats_per_population))

