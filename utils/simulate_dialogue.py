
def simulate_dialogue(game, policy):
  """Simulate a dialogue and returns payoffs for each player."""

  state = game.new_initial_state()

  while not state.is_terminal():
    if state.is_chance_node():
      # Chance node: sample an outcome
      outcomes = state.chance_outcomes()
      action_list, prob_list = zip(*outcomes)
      action = np.random.choice(action_list, p=prob_list)
      state.apply_action(action)
    else:
      # Decision node: sample action for the single current player
      action = policy(state.current_player(), state)
      state.apply_action(action)

  # Game is now done. Print utilities for each player
  returns = state.returns()

  return returns

