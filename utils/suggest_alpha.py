
def suggest_alpha(payoff_tables, tol=.1):
  """Suggests an alpha for use in alpha-rank.

  The suggested alpha is approximately the smallest possible alpha such that
  the ranking has 'settled out'. It is calculated as
  -ln(tol)/min_gap_between_payoffs.

  The logic behind this settling out is that the fixation probabilities can be
  expanded as a series, and the relative size of each term in this series
  changes with alpha. As alpha gets larger and larger, one of the terms in
  this series comes to dominate, and this causes the ranking to settle
  down. Just how fast this domination happens is easy to calculate, and this
  function uses it to estimate the alpha by which the ranking has settled.

  You can find further discussion at the PR:

  https://github.com/deepmind/open_spiel/pull/403

  Args:
    payoff_tables: List of game payoff tables, one for each agent identity. Each
      payoff_table may be either a numpy array, or a _PayoffTableInterface
      object.
    tol: the desired gap between the first and second terms in the fixation
      probability expansion. A smaller tolerance leads to a larger alpha, and
      a 'more settled out' ranking.

  Returns:
    A suggested alpha.
  """
  payoffs_are_hpt_format = utils.check_payoffs_are_hpt(payoff_tables)

  num_strats_per_population = utils.get_num_strats_per_population(
      payoff_tables, payoffs_are_hpt_format)
  num_profiles = utils.get_num_profiles(num_strats_per_population)

  gap = np.inf
  for id_row_profile in range(num_profiles):
    row_profile = utils.get_strat_profile_from_id(num_strats_per_population,
                                                  id_row_profile)

    next_profile_gen = utils.get_valid_next_profiles(num_strats_per_population,
                                                     row_profile)

    for index_population_that_changed, col_profile in next_profile_gen:
      payoff_table_k = payoff_tables[index_population_that_changed]
      f_r = _get_payoff(payoff_table_k, payoffs_are_hpt_format, col_profile,
                        index_population_that_changed)
      f_s = _get_payoff(payoff_table_k, payoffs_are_hpt_format, row_profile,
                        index_population_that_changed)
      if f_r > f_s:
        gap = min(gap, f_r - f_s)

  return -np.log(tol)/gap

