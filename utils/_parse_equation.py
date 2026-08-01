
def _parse_equation(equation: str) -> tuple[list[list[str]], list[list[str]]]:
  """Parses an einshape equation."""
  if equation.count("->") != 1:
    raise ValueError("Equation must contain exactly one '->'")
  lhs_str, rhs_str = equation.split("->")
  return _parse_side(lhs_str), _parse_side(rhs_str)

