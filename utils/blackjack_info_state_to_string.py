
def blackjack_info_state_to_string(state):
  if state.is_terminal():
    return str(state)
  else:
    return (
        "Terminal? False\n"
        f"Dealer visible card: {state.dealers_visible_card()}\n"
        f"Player sum: {state.get_best_player_total(0)}\n"
    )

