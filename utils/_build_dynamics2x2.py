
def _build_dynamics2x2():
  """Build multi-population dynamics."""
  game = pyspiel.load_game("matrix_pd")
  payoff_tensor = utils.game_payoffs_array(game)
  return dynamics.MultiPopulationDynamics(payoff_tensor, dynamics.replicator)

