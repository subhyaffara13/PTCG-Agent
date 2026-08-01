
def _approx_mgce(meta_game, per_player_repeats, ignore_repeats=False,
                 epsilon=0.01):
  """Approximate Maximum Gini CE."""
  a_mat, e_vec, meta = _ace_constraints(
      meta_game, [0.0] * len(per_player_repeats), remove_null=True,
      zero_tolerance=1e-8)
  max_ab = 0.0
  if a_mat.size:
    max_ab = np.max(a_mat.mean(axis=1))
  a_mat, e_vec, meta = _ace_constraints(
      meta_game, [epsilon * max_ab] * len(per_player_repeats), remove_null=True,
      zero_tolerance=1e-8)
  a_mats = _partition_by_player(
      a_mat, meta["p_vec"], len(per_player_repeats))
  e_vecs = _partition_by_player(
      e_vec, meta["p_vec"], len(per_player_repeats))
  dist, _ = _try_two_solvers(
      _qp_ce,
      meta_game, a_mats, e_vecs,
      action_repeats=(None if ignore_repeats else per_player_repeats))
  return dist, dict()

