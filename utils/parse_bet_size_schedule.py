
def parse_bet_size_schedule(bet_size_schedule_str: str) -> list[BetSizeLevel]:
  """Parses a bet-size schedule string into a list of BetSizeLevel objects.

  Parsed bet-size schedule strings are of the form
    <bet_size_level_1>;...;<bet_size_level_n>
  where each bet-size level is of the form
    <num_hands>:<small_bet_size>/<big_bet_size>

  Args:
    bet_size_schedule_str: A string specifying the bet-size schedule. The format
      is a semicolon-separated list of bet-size levels, where each level is a
      colon-separated tuple of `num_hands` & `<small_bet_size>/<big_bet_size>`.

  Returns:
    A list of BetSizeLevel objects parsed from the input string.
  """
  if not bet_size_schedule_str:
    return []

  bet_sizes = []
  levels_str = bet_size_schedule_str.removesuffix(";").split(";")
  for level_str in levels_str:
    parts = level_str.split(":")
    if len(parts) != 2:
      raise ValueError(
          f"Invalid bet-size schedule string: {bet_size_schedule_str}"
      )
    bet_size_parts = parts[1].split("/")
    if len(bet_size_parts) != 2:
      raise ValueError(
          f"Invalid bet-size schedule string: {bet_size_schedule_str}"
      )
    num_hands = int(parts[0])
    small_bet_size = int(bet_size_parts[0])
    big_bet_size = int(bet_size_parts[1])
    bet_sizes.append(BetSizeLevel(num_hands, small_bet_size, big_bet_size))
  return bet_sizes

