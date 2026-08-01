
def _build_dynamics3x3():
  """Build single-population dynamics."""
  game = pyspiel.load_game("matrix_rps")
  payoff_tensor = utils.game_payoffs_array(game)
  return dynamics.SinglePopulationDynamics(payoff_tensor, dynamics.replicator)

