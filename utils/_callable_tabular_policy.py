
def _callable_tabular_policy(tabular_policy):
  """Turns a tabular policy into a callable.

  Args:
    tabular_policy: A dictionary mapping information state key to a dictionary
      of action probabilities (action -> prob).

  Returns:
    A function `state` -> list of (action, prob)
  """

  def wrap(state):
    infostate_key = state.information_state_string(state.current_player())
    assert infostate_key in tabular_policy
    ap_list = []
    for action in state.legal_actions():
      assert action in tabular_policy[infostate_key]
      ap_list.append((action, tabular_policy[infostate_key][action]))
    return ap_list

  return wrap

