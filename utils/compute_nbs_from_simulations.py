
def compute_nbs_from_simulations(game, num_games, bots):
  """Compute empirical NBS from simulations."""
  avg_returns = np.zeros(game.num_players())
  for _ in range(num_games):
    state = game.new_initial_state()
    while not state.is_terminal():
      if state.is_chance_node():
        # Chance node: sample an outcome
        outcomes = state.chance_outcomes()
        action_list, prob_list = zip(*outcomes)
        action = np.random.choice(action_list, p=prob_list)
        state.apply_action(action)
      else:
        player = state.current_player()
        action = bots[player].step(state)
        state.apply_action(action)
    returns = np.asarray(state.returns())
    avg_returns += returns
  avg_returns /= num_games
  return np.prod(avg_returns)

