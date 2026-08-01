
def _full_best_response_policy(br_infoset_dict):
  """Turns a dictionary of best response action selections into a full policy.

  Args:
    br_infoset_dict: A dictionary mapping information state to a best response
      action.

  Returns:
    A function `state` -> list of (action, prob)
  """

  def wrap(state):
    infostate_key = state.information_state_string(state.current_player())
    br_action = br_infoset_dict[infostate_key]
    ap_list = []
    for action in state.legal_actions():
      ap_list.append((action, 1.0 if action == br_action else 0.0))
    return ap_list

  return wrap

