
def play_tic_tac_toe():
  """Solves tic tac toe."""
  game = pyspiel.load_game("tic_tac_toe")

  print("Solving the game; depth_limit = {}".format(-1))
  values = value_iteration.value_iteration(game, -1, 0.01)

  for state, value in values.items():
    print("")
    print(str(state))
    print("Value = {}".format(value))

  initial_state = "...\n...\n..."
  cross_win_state = "...\n...\n.ox"
  naught_win_state = "x..\noo.\nxx."

  assert values[initial_state] == 0, "State should be drawn: \n" + initial_state
  assert values[cross_win_state] == 1, ("State should be won by player 0: \n" +
                                        cross_win_state)
  assert values[naught_win_state] == -1, (
      "State should be won by player 1: \n" + cross_win_state)

