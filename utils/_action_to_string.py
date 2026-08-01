
def _action_to_string(action):
  """Converts OpenSpiel action id (an integer) to a BlueChip action string.

  Args:
    action: an integer action id corresponding to a bid.

  Returns:
    A string in BlueChip format, e.g. 'PASSES' or 'bids 1H', or 'plays ck'.
  """
  if action == _ACTION_PASS:
    return "PASSES"
  elif action == _ACTION_DBL:
    return "DOUBLES"
  elif action == _ACTION_RDBL:
    return "REDOUBLES"
  elif action >= _ACTION_BID:
    level = str((action - _ACTION_BID) // _NUMBER_TRUMP_SUITS + 1)
    trumps = _TRUMP_SUIT[(action - _ACTION_BID) % _NUMBER_TRUMP_SUITS]
    return "bids " + level + trumps
  else:
    rank = action // _NUMBER_SUITS
    suit = action % _NUMBER_SUITS
    return "plays " + _LRANKS[rank] + _LSUIT[suit]


def _action_to_string(action):
  """Converts OpenSpiel action id (an integer) to a BlueChip bid string.

  Args:
    action: an integer action id corresponding to a bid.

  Returns:
    A string in BlueChip format.

  Inverse of `_string_to_action`. See documentation there.
  """
  level = str((action - 1) // _NUMBER_TRUMP_SUITS + 1)
  trumps = _TRUMP_SUIT[(action - 1) % _NUMBER_TRUMP_SUITS]
  return level + trumps

