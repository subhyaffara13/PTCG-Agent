
def simulate_random_game(game: pyspiel.Game):
  """Simulates a game."""
  state = game.new_initial_state()
  while not state.is_terminal():
    # The state can be three different types: chance node,
    # simultaneous node, or decision node
    if state.is_chance_node():
      outcomes = state.chance_outcomes()
      action_list, prob_list = zip(*outcomes)
      action = np.random.choice(action_list, p=prob_list)
      state.apply_action(action)
    elif state.is_simultaneous_node():
      heuristic_value = heuristics.evaluate_state(state, state.current_player())
      print(f"---\nState is: \n{state}\nHeuristic value: {heuristic_value}\n")
      random_choice = lambda a: np.random.choice(a) if a else [0]
      chosen_actions = [
          random_choice(state.legal_actions(pid))
          for pid in range(game.num_players())
      ]
      state.apply_actions(chosen_actions)
    else:
      heuristic_value = heuristics.evaluate_state(state, state.current_player())
      print(f"---\nState is: \n{state}\nHeuristic value: {heuristic_value}\n")
      action = np.random.choice(state.legal_actions(state.current_player()))
      state.apply_action(action)

