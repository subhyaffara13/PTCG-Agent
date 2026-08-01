
def docstring_signature(f):
  """Returns the first line from a docstring - the signature for a function."""
  return f.__doc__.split('\n')[0]

