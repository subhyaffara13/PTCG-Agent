
def build_player_policy(policies):
  def player_policy(player_id, state):
    return policies[player_id](state)
  return player_policy

