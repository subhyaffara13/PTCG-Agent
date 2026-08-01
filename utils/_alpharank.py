
def _alpharank(meta_game, per_player_repeats, ignore_repeats=False):
  """AlphaRank."""
  if not ignore_repeats:
    meta_game = _expand_meta_game(meta_game, per_player_repeats)
  meta_dist = alpharank_lib.sweep_pi_vs_epsilon([mg for mg in meta_game])
  meta_dist[meta_dist < DIST_TOL] = 0.0
  meta_dist /= np.sum(meta_dist)
  meta_dist = np.reshape(meta_dist, meta_game.shape[1:])
  if not ignore_repeats:
    meta_dist = _unexpand_meta_dist(meta_dist, per_player_repeats)
  return meta_dist, dict()

