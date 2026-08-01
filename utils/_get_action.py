
def _get_action(state, action_str):
  for action in state.legal_actions():
    if action_str == state.action_to_string(state.current_player(), action):
      return action
  raise ValueError("invalid action string: {}".format(action_str))


def _get_action(state, action_str):
  for action in state.legal_actions():
    if action_str == state.action_to_string(state.current_player(), action):
      return action
  raise ValueError("invalid action string: {}".format(action_str))


def _get_action(state, action_str):
  """Returns the action integer for a given action string.

  Args:
    state: The current pyspiel state.
    action_str: The string representation of the action (e.g. "x(0,0)").

  Returns:
    The integer action id, or None if not found.
  """
  for action in state.legal_actions():
    if action_str == state.action_to_string(state.current_player(), action):
      return action
  return None

