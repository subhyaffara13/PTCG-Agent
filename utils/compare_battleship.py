
def compare_battleship():
  game_params = {
      "board_height": 2,
      "board_width": 2,
      "num_shots": 4,
      "ship_sizes": "[2]",
      "ship_values": "[1]",
      "allow_repeated_shots": False,
  }
  game = pyspiel.load_game("battleship", game_params)
  compare_cfr_with_jax_cfr(game)

