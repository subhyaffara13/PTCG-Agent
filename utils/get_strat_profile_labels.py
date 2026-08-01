
def get_strat_profile_labels(payoff_tables, payoffs_are_hpt_format):
  """Returns strategy labels corresponding to a payoff_table.

  Namely, for games where strategies have no human-understandable labels
  available, this function returns a labels object corresponding to the
  strategy profiles.

  Examples:
    Generated labels for a single-population game with 3 strategies:
      ['0','1','2'].
    Generated labels for a 3-population game with 2 strategies per population:
      {0: ['0','1'], 1: ['0','1'], 2: ['0','1']}

  Args:
    payoff_tables: List of game payoff tables, one for each agent identity. Each
      payoff_table may be either a 2D numpy array, or a _PayoffTableInterface
      object.
    payoffs_are_hpt_format: Boolean indicating whether each payoff table in
      payoff_tables is a 2D numpy array, or a _PayoffTableInterface object (AKA
      Heuristic Payoff Table or HPT). True indicates HPT format, False indicates
      2D numpy array.

  Returns:
    Strategy labels.
  """

  num_populations = len(payoff_tables)

  if num_populations == 1:
    num_strats_per_population = get_num_strats_per_population(
        payoff_tables, payoffs_are_hpt_format)
    labels = [str(x) for x in range(num_strats_per_population[0])]
  else:
    num_strats_per_population = get_num_strats_per_population(
        payoff_tables, payoffs_are_hpt_format)
    labels = dict()
    label_text = []
    # Construct a list of strategy labels for each population
    for num_strats in num_strats_per_population:
      label_text.append([str(i_strat) for i_strat in range(num_strats)])
    population_ids = range(num_populations)
    labels = dict(zip(population_ids, label_text))

  return labels

