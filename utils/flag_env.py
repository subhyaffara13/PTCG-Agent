
def flag_env(**kwargs):
  """A context manager for setting and restoring flags."""
  old_flags = {kwarg: getattr(flags.FLAGS, kwarg) for kwarg in kwargs}
  for kwarg, new_value in kwargs.items():
    setattr(flags.FLAGS, kwarg, new_value)
  try:
    yield
  finally:
    for kwarg, old_value in old_flags.items():
      setattr(flags.FLAGS, kwarg, old_value)

