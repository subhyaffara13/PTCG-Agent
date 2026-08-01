
def _graph_state_flatten(x: GraphState):
  leaves, static_keys = statelib._state_flatten(x._state)
  return leaves, (x._graphdef, static_keys)

