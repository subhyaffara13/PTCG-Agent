
def _trajectory(line: str):
  """Returns parsed action trajectory."""
  actions = [int(x) for x in line.split(' ')]
  return tuple(actions)

