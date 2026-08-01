
def _unexpand_meta_dist(meta_dist, per_player_repeats):
  num_players = len(meta_dist.shape)
  for player in range(num_players):
    meta_dist = np.add.reduceat(
        meta_dist, [0] + np.cumsum(per_player_repeats[player]).tolist()[:-1],
        axis=player)
  return meta_dist

