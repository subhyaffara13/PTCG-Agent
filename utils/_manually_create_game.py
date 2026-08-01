
def _manually_create_game():
  """Creates the game manually from the spiel building blocks."""
  game_type = pyspiel.GameType(
      "matching_pennies",
      "Matching Pennies",
      pyspiel.GameType.Dynamics.SIMULTANEOUS,
      pyspiel.GameType.ChanceMode.DETERMINISTIC,
      pyspiel.GameType.Information.ONE_SHOT,
      pyspiel.GameType.Utility.ZERO_SUM,
      pyspiel.GameType.RewardModel.TERMINAL,
      2,  # max num players
      2,  # min_num_players
      True,  # provides_information_state
      True,  # provides_information_state_tensor
      False,  # provides_observation
      False,  # provides_observation_tensor
      dict()  # parameter_specification
  )
  game = pyspiel.MatrixGame(
      game_type,
      {},  # game_parameters
      ["Heads", "Tails"],  # row_action_names
      ["Heads", "Tails"],  # col_action_names
      [[-1, 1], [1, -1]],  # row player utilities
      [[1, -1], [-1, 1]]  # col player utilities
  )
  return game

