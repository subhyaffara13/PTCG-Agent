
def convert_to_varargs(sig, *args, **kwargs):
  """Converts varargs+kwargs function arguments into varargs only."""
  bound_args = sig.bind(*args, **kwargs)
  return bound_args.args

