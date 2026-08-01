
def get_kuhn_poker_data(num_players=4, iterations=3):
  """Returns the kuhn poker data for the number of players specified."""
  game = pyspiel.load_game('kuhn_poker', {'players': num_players})
  xfp_solver = fictitious_play.XFPSolver(game, save_oracles=True)
  for _ in range(iterations):
    xfp_solver.iteration()

  # Results are seed-dependent, so show some interesting cases
  if num_players == 2:
    meta_games = xfp_solver.get_empirical_metagame(100, seed=1)
  elif num_players == 3:
    meta_games = xfp_solver.get_empirical_metagame(100, seed=5)
  elif num_players == 4:
    meta_games = xfp_solver.get_empirical_metagame(100, seed=2)

  # Metagame utility matrices for each player
  payoff_tables = []
  for i in range(num_players):
    payoff_tables.append(meta_games[i])
  return payoff_tables


def get_kuhn_poker_data(num_players=3):
  """Returns the kuhn poker data for the number of players specified."""
  game = pyspiel.load_game('kuhn_poker', {'players': num_players})
  xfp_solver = fictitious_play.XFPSolver(game, save_oracles=True)
  for _ in range(3):
    xfp_solver.iteration()

  # Results are seed-dependent, so show some interesting cases
  if num_players == 2:
    meta_games = xfp_solver.get_empirical_metagame(100, seed=1)
  elif num_players == 3:
    meta_games = xfp_solver.get_empirical_metagame(100, seed=5)
  elif num_players == 4:
    meta_games = xfp_solver.get_empirical_metagame(100, seed=2)

  # Metagame utility matrices for each player
  payoff_tables = []
  for i in range(num_players):
    payoff_tables.append(meta_games[i])
  return payoff_tables

