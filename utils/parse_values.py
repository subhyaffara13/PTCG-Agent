
def parse_values(string_values_list: List[str]) -> List[float]:
  """Turn a list of strings into a list of floats."""
  return [parse_value(val) for val in string_values_list]

