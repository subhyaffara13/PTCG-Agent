
def add_meta_dist(
    meta_dists, meta_values, meta_solver, meta_game, per_player_repeats,
    ignore_repeats):
  """Returns meta_dist."""
  num_players = meta_game.shape[0]
  meta_solver_func = FLAG_TO_FUNC[meta_solver]
  meta_dist, _ = meta_solver_func(
      meta_game, per_player_repeats, ignore_repeats=ignore_repeats)
  # Clean dist.
  meta_dist = meta_dist.astype(np.float64)
  meta_dist[meta_dist < DIST_TOL] = 0.0
  meta_dist[meta_dist > 1.0] = 1.0
  meta_dist /= np.sum(meta_dist)
  meta_dist[meta_dist > 1.0] = 1.0
  meta_dists.append(meta_dist)
  meta_value = np.sum(
      meta_dist * meta_game, axis=tuple(range(1, num_players + 1)))
  meta_values.append(meta_value)
  return meta_dist

