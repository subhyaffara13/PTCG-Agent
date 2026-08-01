
def if_args_not_none(fn, *args, **kwargs):
  """Wrap chex assertion to only be evaluated if positional args not `None`."""
  found_none = False
  for x in args:
    found_none = found_none or (x is None)
  if not found_none:
    fn(*args, **kwargs)

