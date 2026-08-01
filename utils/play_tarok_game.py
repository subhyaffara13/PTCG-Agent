
def play_tarok_game():
  game = pyspiel.load_game("tarok(players=3)")
  state = game.new_initial_state()
  while not state.is_terminal():
    print_info(game, state)
    state.apply_action(int(input("Enter action: ")))
    print("-" * 70, "\n")
  print(state.current_game_phase())
  print("Players' scores: {}".format(state.rewards()))

