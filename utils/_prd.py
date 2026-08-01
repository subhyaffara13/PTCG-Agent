
def _prd(meta_game, per_player_repeats, ignore_repeats=False):
  """Projected replicator dynamics."""
  if not ignore_repeats:
    meta_game = _expand_meta_game(meta_game, per_player_repeats)
  meta_dist = projected_replicator_dynamics.projected_replicator_dynamics(
      meta_game)
  labels = string.ascii_lowercase[:len(meta_dist)]
  comma_labels = ",".join(labels)
  meta_dist = np.einsum("{}->{}".format(comma_labels, labels), *meta_dist)
  meta_dist[meta_dist < DIST_TOL] = 0.0
  meta_dist /= np.sum(meta_dist)
  meta_dist = _unexpand_meta_dist(meta_dist, per_player_repeats)
  return meta_dist, dict()

