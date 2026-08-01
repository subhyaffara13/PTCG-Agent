
def compare_goofspiel_descending():
  game_params = {"num_cards": 4, "imp_info": True, "points_order": "descending"}
  game = pyspiel.load_game_as_turn_based("goofspiel", game_params)
  compare_cfr_with_jax_cfr(game)

