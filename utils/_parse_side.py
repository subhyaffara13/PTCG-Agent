
def _parse_side(s: str) -> list[list[str]]:
  """Parses one side of an einshape equation into groups of named dimensions.

  Groups are indicated by parentheses. Dimensions outside of parentheses are
  treated as groups of size 1.
  For example:
    "a(bc)d" -> [['a'], ['b', 'c'], ['d']]
    "(ab)c" -> [['a', 'b'], ['c']]

  Args:
    s: One side of an einshape equation string.

  Returns:
    A list of lists of characters, where each inner list represents a group of
    dimensions.
  """
  # Remove spaces
  s = s.replace(" ", "")
  groups = []
  i = 0
  while i < len(s):
    if s[i] == "(":
      # Start of a group
      j = s.find(")", i)
      if j == -1:
        raise ValueError(f"Unmatched parenthesis in {s!r}")
      group = list(s[i + 1 : j])
      groups.append(group)
      i = j + 1
    elif s[i] == ")":
      raise ValueError(f"Unmatched parenthesis in {s!r}")
    else:
      # distinct dimension
      groups.append([s[i]])
      i += 1
  return groups

