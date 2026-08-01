
def print_info(unused_game, state):
  """Print information about the game state."""
  print("Game phase: {}".format(state.current_game_phase()))
  print("Selected contract: {}".format(state.selected_contract()))
  print("Current player: {}".format(state.current_player()))
  player_cards = state.player_cards(state.current_player())
  action_names = [state.card_action_to_string(a) for a in player_cards]
  print("\nPlayer cards: {}".format(
      list(zip(action_names, player_cards))))

  if state.current_game_phase() == pyspiel.TarokGamePhase.TALON_EXCHANGE:
    print_talon_exchange_info(state)
  elif state.current_game_phase() == pyspiel.TarokGamePhase.TRICKS_PLAYING:
    print_tricks_playing_info(state)
  else:
    print()

  legal_actions = state.legal_actions()
  action_names = [state.action_to_string(a) for a in state.legal_actions()]
  print("Legal actions: {}\n".format(
      list(zip(action_names, legal_actions))))

