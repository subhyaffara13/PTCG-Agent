
def get_soccer_data():
  """Returns the payoffs and strategy labels for MuJoCo soccer experiments."""
  payoff_file = file_utils.find_file(
      'open_spiel/data/paper_data/response_graph_ucb/soccer.txt', 2)
  payoffs = np.loadtxt(payoff_file)
  return payoffs

