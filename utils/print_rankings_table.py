
def print_rankings_table(payoff_tables,
                         pi,
                         strat_labels,
                         num_top_strats_to_print=8):
  """Prints nicely-formatted table of strategy rankings.

  Args:
    payoff_tables: List of game payoff tables, one for each agent identity. Each
      payoff_table may be either a 2D numpy array, or a _PayoffTableInterface
      object.
    pi: Finite-population Markov chain stationary distribution.
    strat_labels: Strategy labels.
    num_top_strats_to_print: Number of top strategies to print.
  """

  num_populations = len(payoff_tables)
  payoffs_are_hpt_format = check_payoffs_are_hpt(payoff_tables)
  num_strats_per_population = get_num_strats_per_population(
      payoff_tables, payoffs_are_hpt_format)

  # More than total number of strats requested for printing, compute top and
  # use an extra row to indicate additional strategies not shown.
  row_for_lowrank_strats = True
  if num_top_strats_to_print >= len(pi):
    num_top_strats_to_print = len(pi)
    row_for_lowrank_strats = False

  # Cluster strategies according to stationary distr. (in case of tied ranks)
  masses_to_strats = cluster_strats(pi)

  def print_3col(col1, col2, col3):
    print("%-12s %-12s %-12s" % (col1, col2, col3))

  print_3col("Agent", "Rank", "Score")
  print_3col("-----", "----", "-----")

  rank = 1
  num_strats_printed = 0
  # Print a table of strategy rankings from highest to lowest mass
  for _, strats in sorted(masses_to_strats.items(), reverse=True):
    for strat in strats:
      if num_strats_printed >= num_top_strats_to_print:
        break
      rounded_pi = np.round(pi[strat], decimals=2)
      if num_populations == 1:
        strat_profile = strat
      else:
        strat_profile = get_strat_profile_from_id(num_strats_per_population,
                                                  strat)
      label = get_label_from_strat_profile(num_populations, strat_profile,
                                           strat_labels)
      print_3col(label, str(rank), str(np.abs(rounded_pi)))
      num_strats_printed += 1
    rank += 1
    if num_strats_printed >= num_top_strats_to_print:
      break

  # Ellipses to signify additional low-rank strategies are not printed
  if row_for_lowrank_strats:
    print_3col("...", "...", "...")

