
def compare_goofspiel_randomized():
  game_params = {"num_cards": 3, "imp_info": True, "points_order": "random"}
  game = pyspiel.load_game_as_turn_based("goofspiel", game_params)
  compare_cfr_with_jax_cfr(game)

