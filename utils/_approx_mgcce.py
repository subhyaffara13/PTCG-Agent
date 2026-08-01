
def _approx_mgcce(meta_game, per_player_repeats, ignore_repeats=False,
                  epsilon=0.01):
  """Maximum Gini CCE."""
  a_mat, meta = _cce_constraints(
      meta_game, [0.0] * len(per_player_repeats), remove_null=True,
      zero_tolerance=1e-8)
  max_ab = 0.0
  if a_mat.size:
    max_ab = np.max(a_mat.mean(axis=1))
  a_mat, meta = _cce_constraints(
      meta_game, [epsilon * max_ab] * len(per_player_repeats), remove_null=True,
      zero_tolerance=1e-8)
  a_mats = _partition_by_player(
      a_mat, meta["p_vec"], len(per_player_repeats))
  dist, _ = _try_two_solvers(
      _qp_cce,
      meta_game, a_mats, [0.0] * len(per_player_repeats),
      action_repeats=(None if ignore_repeats else per_player_repeats))
  return dist, dict()

