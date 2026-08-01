
def _import_data_create_game():
  """Creates a game via imported payoff data."""
  payoff_file = file_utils.find_file(
      "open_spiel/data/paper_data/response_graph_ucb/soccer.txt", 2)
  payoffs = np.loadtxt(payoff_file)*2-1
  return pyspiel.create_matrix_game(payoffs, payoffs.T)

