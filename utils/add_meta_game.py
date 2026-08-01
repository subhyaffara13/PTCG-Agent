
def add_meta_game(
    meta_games,
    per_player_policies,
    joint_returns):
  """Returns a meta-game tensor."""
  per_player_num_policies = [
      len(policies) for policies in per_player_policies]
  shape = [len(per_player_num_policies)] + per_player_num_policies
  meta_game = np.zeros(shape)
  for pids in itertools.product(*[
      range(np_) for np_ in per_player_num_policies]):
    meta_game[(slice(None),) + pids] = joint_returns[pids]
  meta_games.append(meta_game)
  return meta_games

