
def _RoundTowardZero(value, divider):
  """Truncates the remainder part after division."""
  # For some languages, the sign of the remainder is implementation
  # dependent if any of the operands is negative. Here we enforce
  # "rounded toward zero" semantics. For example, for (-5) / 2 an
  # implementation may give -3 as the result with the remainder being
  # 1. This function ensures we always return -2 (closer to zero).
  result = value // divider
  remainder = value % divider
  if result < 0 and remainder > 0:
    return result + 1
  else:
    return result

