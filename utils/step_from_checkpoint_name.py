import re

def step_from_checkpoint_name(name: str) -> int:
  """Returns the step from a checkpoint name. Also works for tmp checkpoints."""
  if name.isdigit():
    return int(name)
  elif m := re.fullmatch(ALLOWED_STEP_NAME_PATTERN, name):
    return int(m.group(2))
  elif tmp_match := re.match(TMP_DIR_STEP_PATTERN, name):
    return int(tmp_match.group(1))
  raise ValueError(f'Unrecognized name format: {name}.')

