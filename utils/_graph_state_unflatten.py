
def _graph_state_unflatten(static_data, leaves):
  graphdef, static_keys = static_data
  state = statelib._state_unflatten(State, static_keys, leaves)
  return GraphState(graphdef, state)

