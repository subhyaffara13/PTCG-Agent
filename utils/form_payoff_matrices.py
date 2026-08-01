
def form_payoff_matrices(game_results, num_checkpts):
  """Packages dictionary of game results into a payoff tensor.

  Args:
    game_results: dictionary of payoffs for each game evaluated, keys are
      (pair, profile) where pair is a tuple of the two agents played against
      each other and profile indicates pure joint action played by all agents
    num_checkpts: list of ints, number of strats (or ckpts) per player
  Returns:
    payoff_matrices: dict of np.arrays (2 x num_checkpts x num_checkpts) with
      payoffs for two players. keys are pairs above with lowest index agent
      first
  """
  num_players = len(num_checkpts)
  payoff_matrices = {}
  for pi, pj in itertools.combinations(range(num_players), 2):
    key = (pi, pj)
    payoff_matrices[key] = np.zeros((2, num_checkpts[pi], num_checkpts[pj]))
  for key_profile, payoffs in game_results.items():
    key, profile = key_profile
    i, j = key
    ai = profile[i]
    aj = profile[j]
    payoff_matrices[key][0, ai, aj] = payoffs[i]
    payoff_matrices[key][1, ai, aj] = payoffs[j]
  return payoff_matrices


def form_payoff_matrices(game_results, num_checkpts):
  """Packages dictionary of game results into a payoff tensor.

  Args:
    game_results: dictionary of payoffs for each game evaluated
    num_checkpts: int, number of strats (or ckpts) per player
  Returns:
    payoff_matrices: np.array (2 x num_checkpts x num_checkpts) with payoffs for
      two players (assumes symmetric game and only info for 2 players is needed
      for stochastic gradients)
  """
  payoff_matrices = np.zeros((2, num_checkpts, num_checkpts))
  for profile, payoffs in game_results.items():
    i, j = profile[:2]
    payoff_matrices[:, i, j] = payoffs[:2]
  return payoff_matrices

