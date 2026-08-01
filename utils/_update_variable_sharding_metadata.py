
def _update_variable_sharding_metadata(
    tree, transform_metadata, axis_fn: AxisFn
):
  def _update_axes_fn(node_states):
    if isinstance(node_states, extract.NodeStates) and isinstance(
      node_states.metadata, (StateAxes, int)
    ):
      if isinstance(node_states.metadata, int):
        state = node_states.state
        assert isinstance(state, State | variablelib.Variable)
        state = axis_fn(state, node_states.metadata, transform_metadata)
        return node_states.replace(states=(state,))
      else:
        states_out: list[State | variablelib.Variable] = []
        for state, axis in zip(node_states.states, node_states.metadata.axes):
          assert isinstance(state, State | variablelib.Variable)
          if isinstance(axis, int):
            state = axis_fn(state, axis, transform_metadata)
          states_out.append(state)
        return node_states.replace(states=tuple(states_out))
    return node_states

  return jax.tree.map(
    _update_axes_fn, tree, is_leaf=lambda x: isinstance(x, extract.NodeStates)
  )

