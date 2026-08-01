
def parse_blind_schedule(blind_schedule_str: str) -> list[BlindLevel]:
  """Parses a blind schedule string into a list of BlindLevel objects.

  Port of ParseBlindSchedule from repeated_poker.cc.

  Parses blind schedule string of the form
    <blind_level_1>;...;<blind_level_n>
  where each blind level is of the form
    <num_hands>:<small_blind>/<big_blind>

  Args:
    blind_schedule_str: A string specifying the blind schedule. The format is a
      semicolon-separated list of blind levels, where each level is a
      colon-separated tuple of `num_hands` and `<small_blind>/<big_blind>`.

  Returns:
    A list of BlindLevel objects parsed from the input string.
  """
  if not blind_schedule_str:
    return []

  blind_levels = []
  levels_str = blind_schedule_str.removesuffix(";").split(";")
  for level_str in levels_str:
    parts = level_str.split(":")
    if len(parts) != 2:
      raise ValueError(f"Invalid blind schedule string: {blind_schedule_str}")
    blinds = parts[1].split("/")
    if len(blinds) != 2:
      raise ValueError(f"Invalid blind schedule string: {blind_schedule_str}")
    num_hands = int(parts[0])
    small_blind = int(blinds[0])
    big_blind = int(blinds[1])
    blind_levels.append(
        BlindLevel(
            num_hands,
            small_blind,
            big_blind,
        )
    )
  return blind_levels

