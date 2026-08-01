
def play_game(state: pyspiel.State,
              bots: list[pyspiel.Bot]):
  """Play the game via console."""

  while not state.is_terminal():
    print(f"State: \n{state}\n")
    if state.is_chance_node():
      outcomes = state.chance_outcomes()
      action_list, prob_list = zip(*outcomes)
      outcome = np.random.choice(action_list, p=prob_list)
      print(f"Chance chose: {outcome} ({state.action_to_string(outcome)})")
      state.apply_action(outcome)
    else:
      player = state.current_player()
      action = bots[player].step(state)
      print(f"Chose action: {action} ({state.action_to_string(action)})")
      state.apply_action(action)

  print("\n-=- Game over -=-\n")
  print(f"Terminal state:\n{state}")
  print(f"Returns: {state.returns()}")
  return

