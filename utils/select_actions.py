
def select_actions(observations, cur_player):
  cur_legal_actions = observations["legal_actions"][cur_player]
  actions = [np.random.choice(cur_legal_actions)]
  return actions

