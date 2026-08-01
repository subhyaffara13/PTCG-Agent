
def parse_bring_in_schedule(bring_in_schedule_str: str) -> list[BringInLevel]:
  """Parses a bring-in schedule string into a list of BringInLevel objects.

  Parsed bring-in schedule strings are of the form
    <bring_in_level_1>;...;<bring_in_level_n>
  where each bring-in level is of the form
    <num_hands>:<bring_in>

  Args:
    bring_in_schedule_str: A string specifying the bring-in schedule. The format
      is a semicolon-separated list of bring-in levels, where each level is a
      colon-separated tuple of `num_hands` and `bring_in`.

  Returns:
    A list of BringInLevel objects parsed from the input string.
  """
  if not bring_in_schedule_str:
    return []
  bring_ins = []
  levels_str = bring_in_schedule_str.removesuffix(";").split(";")
  for level_str in levels_str:
    parts = level_str.split(":")
    if len(parts) != 2:
      raise ValueError(
          f"Invalid bring-in schedule string: {bring_in_schedule_str}"
      )
    num_hands = int(parts[0])
    bring_in = int(parts[1])
    bring_ins.append(BringInLevel(num_hands, bring_in))
  return bring_ins

