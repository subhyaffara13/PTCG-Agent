
def _rmwcce(meta_game, per_player_repeats, ignore_repeats=False):
  """Random maximum welfare CCE."""
  del ignore_repeats
  num_players = len(per_player_repeats)
  cost = np.ravel(np.sum(meta_game, axis=0))
  cost += np.ravel(np.random.normal(size=meta_game.shape[1:])) * 1e-6
  a_mat, _ = _cce_constraints(
      meta_game, [0.0] * num_players, remove_null=True,
      zero_tolerance=1e-8)
  e_vec = np.zeros([a_mat.shape[0]])
  x, _ = _linear(meta_game, a_mat, e_vec, cost=cost)
  dist = np.reshape(x, meta_game.shape[1:])
  return dist, dict()

