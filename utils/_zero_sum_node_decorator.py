
def _zero_sum_node_decorator(state):
  """Custom node decorator that only shows the return of the first player."""
  attrs = treeviz.default_node_decorator(state)  # get default attributes
  if state.is_terminal():
    attrs["label"] = str(int(state.returns()[0]))
  return attrs

