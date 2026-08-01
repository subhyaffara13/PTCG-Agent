
def _is_batching(factor: str) -> bool:
  """Checks if a factor is a representation for leading batching dimensions.

  Leading batching dimensions is represented by a factor containing ... and
     optionally followed by a digit, and ... is equivalent to ...0.
  """
  if len(factor) < 1 or factor[0] != BATCHING:
    return False
  return len(factor) == 1 or factor[1:].isdigit()

