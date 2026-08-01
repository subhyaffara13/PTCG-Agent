
def _expand_meta_game(meta_game, per_player_repeats):
  num_players = meta_game.shape[0]
  for player in range(num_players):
    meta_game = np.repeat(meta_game, per_player_repeats[player], axis=player+1)
  return meta_game

