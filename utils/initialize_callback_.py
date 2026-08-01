
def initialize_callback_(
    iteration,
    per_player_repeats,
    per_player_policies,
    joint_policies,
    joint_returns,
    meta_games,
    train_meta_dists,
    eval_meta_dists,
    train_meta_values,
    eval_meta_values,
    train_meta_gaps,
    eval_meta_gaps,
    game):
  """Callback which allows initializing from checkpoint."""
  del game
  checkpoint = None
  return (
      iteration,
      per_player_repeats,
      per_player_policies,
      joint_policies,
      joint_returns,
      meta_games,
      train_meta_dists,
      eval_meta_dists,
      train_meta_values,
      eval_meta_values,
      train_meta_gaps,
      eval_meta_gaps,
      checkpoint)

