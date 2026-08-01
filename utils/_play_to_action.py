
def _play_to_action(action_str):
  """Returns an OpenSpiel action id (an integer) from a BlueChip card string."""
  rank = _LRANKS.index(action_str[0])
  suit = _LSUIT.index(action_str[1])
  return rank * _NUMBER_SUITS + suit

