
def _reached_desired_step(step: int, until_step: Optional[int]) -> bool:
  if step is None:
    return False
  elif until_step is None:
    return True
  elif step >= until_step:
    return True
  return False

