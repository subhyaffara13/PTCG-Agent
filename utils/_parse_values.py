
def _parse_values(param_str) -> list[int | decimal.Decimal]:
  """Convert " "-separated values in a ``str`` to numerical values via pokerkit.

  Args:
    param_str: A space-separated string of numerical values.

  Returns:
    A list of numerical values, which can be either `int` or `decimal.Decimal`.
  """
  if not param_str:
    return None
  return [pokerkit.parse_value(s) for s in param_str.split(" ")]


def _parse_values(
    rule: str,
) -> tuple[ArrayMapping, ...]:
  """Parses the LHS or RHS of an Einsum notation like string.

  Converts each operand or result in the Einsum notation like string to a tuple
  of ArrayMapping. This very closely follows how einops parses their rules in
  einops/parsing.py.

  Args:
    rule: The Einsum notation for the operands or results of an operation.

  Returns:
    The tuple of ArrayMapping.

  Raises:
    ValueError: If the rule is not balanced or contains unknown characters.
  """

  # Remove unnecessary spaces in the rule to simplify the parsing process.
  words = rule.split()
  rule = " ".join(words)

  # Similar to einops rules, an empty LHS/RHS has a single scalar value.
  if not rule:
    return (ArrayMapping(),)

  all_values = []
  # Represent all dimensions of an value. When an value[0]==BATCHING, the
  # value may have 0 or more leading dimensions.
  value = []
  current_factor: str | None = None
  # A value of None indicates the current dimension is not a compound dimension,
  # while a value of [] indicates that we have just started parsing a compound
  # dimension.
  current_compound_dim: list[str] | None = None

  def add_factor(x):
    if current_compound_dim is None:
      value.append(x)
    else:
      current_compound_dim.append(x)

  rule_len = len(rule)
  rule_index = 0
  while rule_index < rule_len:
    char = rule[rule_index]
    rule_index += 1
    if char == BATCHING:
      if (current_factor is not None or current_compound_dim is not None
          or value):
        raise ValueError(
            "Ellipsis can only be used at the beginning of a dimension")
      if rule_index < rule_len and rule[rule_index].isdigit():
        batching_group_str = ""
        while rule_index < rule_len and rule[rule_index].isdigit():
          batching_group_str += rule[rule_index]
          rule_index += 1
        batching_group = str(int(batching_group_str))
      else:
        batching_group = "0"

      add_factor(f"{BATCHING}{batching_group}")
      continue
    if char in "(), ":
      if current_factor is not None:
        add_factor(current_factor)
        current_factor = None
      if char == "(":
        if current_compound_dim is not None:
          raise ValueError(
              "Compound factors should be one level, nested brackets are not"
              " allowed")
        current_compound_dim = []
      elif char == ")":
        if current_compound_dim is None:
          raise ValueError("Brackets are not balanced")
        if len(current_compound_dim) <= 1:
          raise ValueError("Brackets should contain at least two factors")
        value.append(CompoundFactor(*current_compound_dim))
        current_compound_dim = None
      elif char == ",":
        all_values.append(ArrayMapping(*value))
        value = []
    elif char == "_" or char.isdigit() or char.isalpha():
      if current_factor is None:
        if str.isdigit(char):
          raise ValueError(f"Factor names have to start with a letter, but got '{char}'")
        current_factor = char
      else:
        current_factor += char
    else:
      raise ValueError(f"Unknown character '{char}'")

  if current_compound_dim is not None:
    raise ValueError(f"Brackets are not balanced in rule: '{rule}'")
  if current_factor is not None:
    add_factor(current_factor)
  all_values.append(ArrayMapping(*value))

  return tuple(all_values)

