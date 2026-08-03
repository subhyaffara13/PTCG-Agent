from typing import Optional

def step_prefix_with_underscore(step_prefix: Optional[str]) -> str:
  """Returns `step_prefix` appended with `underscore` or <empty> if None."""
  return '' if step_prefix is None else f'{step_prefix}_'

