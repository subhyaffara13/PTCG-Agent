
def get_spec_var(depth):
  """Returns the name of variable for spec with given depth."""
  return "s" if depth == 0 else "s{}".format(depth)

