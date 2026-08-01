
def print_talon_exchange_info(state):
  talon = [[state.card_action_to_string(x) for x in talon_set]
           for talon_set in state.talon_sets()]
  print("\nTalon: {}\n".format(talon))

