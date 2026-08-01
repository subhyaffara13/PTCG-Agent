
def _graph_state_flatten_with_keys(x: GraphState):
  children, static_keys = statelib._state_flatten_with_keys(x._state)
  return children, (x._graphdef, static_keys)

