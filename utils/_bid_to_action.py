
def _bid_to_action(action_str):
  """Returns an OpenSpiel action id (an integer) from a BlueChip bid string."""
  level = int(action_str[0])
  trumps = _TRUMP_SUIT.index(action_str[1:])
  return _ACTION_BID + (level - 1) * _NUMBER_TRUMP_SUITS + trumps

