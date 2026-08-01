
def _mwce(meta_game, per_player_repeats, ignore_repeats=False):
  """Maximum welfare CE."""
  del ignore_repeats
  num_players = len(per_player_repeats)
  cost = np.ravel(np.sum(meta_game, axis=0))
  a_mat, e_vec, _ = _ace_constraints(
      meta_game, [0.0] * num_players, remove_null=True,
      zero_tolerance=1e-8)
  x, _ = _linear(meta_game, a_mat, e_vec, cost=cost)
  dist = np.reshape(x, meta_game.shape[1:])
  return dist, dict()

