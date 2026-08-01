
def print_tricks_playing_info(state):
  trick_cards = state.trick_cards()
  action_names = [state.card_action_to_string(a) for a in trick_cards]
  print("\nTrick cards: {}\n".format(
      list(zip(action_names, trick_cards))))

