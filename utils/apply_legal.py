
def apply_legal(state, move):
  action = state.parse_move_to_action(move)
  if action in state.legal_actions():
    state.apply_action(action)
  else:
    raise ValueError()

