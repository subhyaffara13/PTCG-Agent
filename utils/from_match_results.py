
def from_match_results(df, consider_agents):
  """Builds a heuristic payoff table from average win probabilities.

  Args:
    df: a Pandas dataframe of match results. Must contain a column "agents"
      consisting of tuples of agent names, and a column "scores" consisting of
      the score for each agent in the match.
    consider_agents: a list of agent names. Will only consider matches in which
      exclusively these agents appeared.

  Returns:
    A PayoffTable object.

  Raises:
    ValueError: if dataframe is empty, or columns 'agents' and 'scores' not
    specified, or games have zero players.
  """
  if df.empty:
    raise ValueError("Please provide a non-empty dataframe.")
  if "agents" not in df.columns:
    raise ValueError("Dataframe must contain a column 'agents'.")
  if "scores" not in df.columns:
    raise ValueError("Dataframe must contain a column 'scores'.")

  num_strategies = len(consider_agents)
  num_players = len(df["agents"][0])

  if num_players == 0:
    raise ValueError("Games must have > 0 players.")

  count_per_distribution = {}
  win_prob_per_distribution = {}

  for i, row in df.iterrows():
    print("Parsing row {} / {} ...".format(i, len(df)), end="\r")
    agents = row["agents"]
    scores = row["scores"]
    assert len(agents) == len(scores) == num_players

    if not set(agents).issubset(set(consider_agents)):
      # Ignore agents outside those we are supposed to consider.
      continue
    elif len(set(agents)) == 1:
      # Special case of self-play: deal with separately.
      continue

    # Find winner(s): In each match one must determine a winning strategy. One
    # way of doing this is to average over the returns for each strategy and
    # then say that the one with the greatest returns is the winner.

    # Get unique score per agent by averaging.
    count_per_agent = collections.defaultdict(int)
    average_score_per_agent = collections.defaultdict(int)
    for agent, score in zip(agents, scores):
      count_per_agent[agent], average_score_per_agent[agent] = _inc_average(
          count_per_agent[agent], average_score_per_agent[agent], score)

    winner_score = max(average_score_per_agent.values())
    winner_agents = [
        k for k, v in average_score_per_agent.items() if v == winner_score
    ]
    winner_strategy_idxs = [
        consider_agents.index(winner) for winner in winner_agents
    ]

    # Select the winner as the one maximizing the selected statistics.
    win_probabilities = np.zeros(num_strategies)
    for winner_strategy_idx in winner_strategy_idxs:
      win_probabilities[winner_strategy_idx] = 1 / len(winner_strategy_idxs)

    distribution = np.zeros(num_strategies)
    for agent, count in count_per_agent.items():
      strategy_idx = consider_agents.index(agent)
      distribution[strategy_idx] = count

    distribution = tuple(distribution)

    if distribution not in count_per_distribution:
      count_per_distribution[distribution] = 1
      win_prob_per_distribution[distribution] = win_probabilities
      continue
    (count_per_distribution[distribution],
     win_prob_per_distribution[distribution]) = _inc_average(
         count_per_distribution[distribution],
         win_prob_per_distribution[distribution], win_probabilities)

  # Populate self-play case (strategy both wins and loses).
  for idx, agent in enumerate(consider_agents):
    distribution = np.zeros(num_strategies)
    distribution[idx] = num_players
    distribution = tuple(distribution)
    win_prob = np.zeros(num_strategies)
    win_prob[idx] = 0.5
    win_prob_per_distribution[distribution] = win_prob

  # Create empty (nan) payoff table.
  table = PayoffTable(num_players, num_strategies)

  # Populate with win probabilities.
  for distribution, payoff in win_prob_per_distribution.items():
    table[distribution] = payoff

  return table

