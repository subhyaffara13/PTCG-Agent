
def _min_epsilon_mgcce(meta_game, per_player_repeats, ignore_repeats=False):
  """Min Epsilon Maximum Gini CCE."""
  a_mat, meta = _cce_constraints(
      meta_game, [0.0] * len(per_player_repeats), remove_null=True,
      zero_tolerance=1e-8)
  a_mats = _partition_by_player(
      a_mat, meta["p_vec"], len(per_player_repeats))
  dist, _ = _try_two_solvers(
      _qp_cce,
      meta_game, a_mats, [0.0] * len(per_player_repeats),
      action_repeats=(None if ignore_repeats else per_player_repeats),
      min_epsilon=True)
  return dist, dict()

