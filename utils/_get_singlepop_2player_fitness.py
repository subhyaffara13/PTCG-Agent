
def _get_singlepop_2player_fitness(payoff_table, payoffs_are_hpt_format, m,
                                   my_popsize, my_strat, opponent_strat,
                                   use_local_selection_model):
  """Gets a target agent fitness given a finite population of competitors.

  Note that this is only applicable to 2-player symmetric games.
  Namely, gets fitness of an agent i playing my_strat in underlying population
  of (my_popsize agents playing my_strat) and (m-my_popsize agents playing
  opponent_strat).

  Args:
    payoff_table: A payoff table.
    payoffs_are_hpt_format: Boolean indicating whether payoff_table is a
      _PayoffTableInterface object (AKA Heuristic Payoff Table or HPT), or a
      numpy array. True indicates HPT format, False indicates numpy array.
    m: The total number of agents in the population.
    my_popsize: The number of agents in the population playing my strategy.
    my_strat: Index of my strategy.
    opponent_strat: Index of the opposing strategy.
    use_local_selection_model: Enable local evolutionary selection model, which
      considers fitness against the current opponent only, rather than the
      global population state.

  Returns:
    The fitness of agent i.
  """

  if use_local_selection_model:
    fitness = payoff_table[tuple([my_strat, opponent_strat])]
  else:
    fitness = ((my_popsize-1)/(m-1)*
               _get_payoff(payoff_table, payoffs_are_hpt_format,
                           strat_profile=[my_strat, my_strat], k=0) +
               (m-my_popsize)/(m-1)*
               _get_payoff(payoff_table, payoffs_are_hpt_format,
                           strat_profile=[my_strat, opponent_strat], k=0))
  return fitness

