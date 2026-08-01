
def _min_epsilon_mgce(meta_game, per_player_repeats, ignore_repeats=False):
  """Min Epsilon Maximum Gini CE."""
  a_mat, e_vec, meta = _ace_constraints(
      meta_game, [0.0] * len(per_player_repeats), remove_null=True,
      zero_tolerance=1e-8)
  a_mats = _partition_by_player(
      a_mat, meta["p_vec"], len(per_player_repeats))
  e_vecs = _partition_by_player(
      e_vec, meta["p_vec"], len(per_player_repeats))
  dist, _ = _try_two_solvers(
      _qp_ce,
      meta_game, a_mats, e_vecs,
      action_repeats=(None if ignore_repeats else per_player_repeats),
      min_epsilon=True)
  return dist, dict()

