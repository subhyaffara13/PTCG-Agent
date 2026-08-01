
def _check_factor(factor:str):
  """Validates a factor.

  A factor is a string starting with a letter and containing only letters,
  digits, or underscores.
  """
  if not factor[0].isalpha():
    raise ValueError(f"Factor names have to start with a letter, but got '{factor[0]}'")
  for char in factor[1:]:
    if char != "_" and not char.isdigit() and not char.isalpha():
      raise ValueError(f"Unknown character '{char}'")

