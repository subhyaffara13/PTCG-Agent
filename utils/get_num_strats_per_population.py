
def get_num_strats_per_population(payoff_tables, payoffs_are_hpt_format):
  """Returns a [num_populations] array of the num.

  of strategies per population.

  E.g., for a 3 population game, this returns
    [num_strats_population1, num_strats_population2, num_strats_population3]

  Args:
    payoff_tables: List of game payoff tables, one for each agent identity. Each
      payoff_table may be either a 2D numpy array, or a _PayoffTableInterface
      object.
    payoffs_are_hpt_format: True indicates HPT format (i.e.
      _PayoffTableInterface object, False indicates 2D numpy array.
  """

  if payoffs_are_hpt_format:
    return np.asarray(
        [payoff_table.num_strategies for payoff_table in payoff_tables])
  else:
    # Non-HPT payoffs are matrices, so can directly return the payoff size
    return np.asarray(np.shape(payoff_tables[0]))

