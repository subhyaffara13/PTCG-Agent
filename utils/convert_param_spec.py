
def convert_param_spec(param_spec):
  """Converts 'size:10;200' into ('size', [10, 200])."""
  split = param_spec.split(':', 2)
  return split[0], [int(v) for v in split[1].split(';')]

