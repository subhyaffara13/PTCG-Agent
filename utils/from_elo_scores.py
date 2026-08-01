
def from_elo_scores(elo_ratings, num_agents=2):
  """Computes the Elo win probability payoff matrix `X` from the Elo scores.

  Args:
    elo_ratings: The elo scores vector of length [num_strategies].
    num_agents: The number of agents. Only 2 agents are supported for now.

  Returns:
    The HPT associated to the Elo win probability payoff matrix `X`. The score
    for a given agent is given by its win probability given its Elo score.

  Raises:
    ValueError: If `num_agents != 2`.
  """
  if num_agents != 2:
    raise ValueError("Only 2 agents are supported, because we need to compute "
                     "the win probability and that can only be computed with "
                     "2 players.")
  num_strategies = len(elo_ratings)

  hpt_rows = []

  possible_teams = utils.distribute(num_agents, num_strategies, normalize=False)

  for distribution_row in possible_teams:
    payoff_row = np.zeros([num_strategies])
    non_zero_index = np.nonzero(distribution_row)[0]  # Why [0]?
    assert len(non_zero_index.shape) == 1

    if len(non_zero_index) > 1:
      index_first_player, index_second_player = non_zero_index
      prob = _compute_win_probability_from_elo(elo_ratings[index_first_player],
                                               elo_ratings[index_second_player])
      payoff_row[index_first_player] = prob
      payoff_row[index_second_player] = 1 - prob
    elif len(non_zero_index) == 1:
      payoff_row[non_zero_index[0]] = 0.5
    else:
      assert False, "Impossible case, we have at least one strategy used."

    hpt_rows.append(np.hstack([distribution_row, payoff_row]))

  return NumpyPayoffTable(np.vstack(hpt_rows))

