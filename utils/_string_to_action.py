
def _string_to_action(call_str):
  """Converts a BlueChip bid string to an OpenSpiel action id (an integer).

  Args:
    call_str: string representing a bid in the BlueChip format, i.e. "[level]
      (as a digit) + [trump suit (S, H, D, C or NT)]", e.g. "1C".

  Returns:
    An integer action id - see `bridge_uncontested_bidding.cc`, functions
    `Denomination` and `Level`.
    0 is reserved for Pass, so bids are in order from 1 upwards: 1 = 1C,
    2 = 1D, etc.
  """
  level = int(call_str[0])
  trumps = _TRUMP_SUIT.index(call_str[1:])
  return (level - 1) * _NUMBER_TRUMP_SUITS + trumps + 1

