
def _scan_split_out(
  carry_deque: PytreeDeque[list[State | variablelib.Variable]],
  graphdefs_deque: PytreeDeque[graphlib.GraphDef],
  broadcast_deque: PytreeDeque[list[State | variablelib.Variable]],
  /,
  ctx: graphlib.SplitContext,
  path: extract.KeyPath,
  prefix,
  x,
):
  assert isinstance(path[0], jax.tree_util.SequenceKey)
  is_input_arg = path[0].idx == 0

  if graphlib.is_graph_node(x) or isinstance(x, variablelib.Variable):
    vectorized_states: list[State | variablelib.Variable] = []
    carry_states: list[State | variablelib.Variable] = []
    broadcast_states: list[State | variablelib.Variable] = []
    if isinstance(prefix, StateAxes):
      graphdef, *states = ctx.split(x, *prefix.filters)

      for state, filter, axis in zip(states, prefix.filters, prefix.axes):
        if axis is None:
          assert is_input_arg  # validated by _check_out_axes
          broadcast_states.append(state)
        elif isinstance(axis, int):
          vectorized_states.append(state)
        elif axis is Carry:
          assert is_input_arg  # validated by _check_out_axes
          carry_states.append(state)
        else:
          obj_repr = 'args' if is_input_arg else 'out'
          raise ValueError(
            f'Invalid axes {axis} for filter {filter} at '
            f'{obj_repr}{jax.tree_util.keystr(path)}'
          )

      if not vectorized_states:
        vectorized_states.append(State({}))
      if is_input_arg:
        carry_deque.append(carry_states)
        broadcast_deque.append(broadcast_states)
      graphdefs_deque.append(graphdef)
      return extract.NodeStates.from_split(
        None, *vectorized_states, metadata=prefix
      )
    elif isinstance(prefix, int):
      graphdef, state = ctx.split(x)
      vectorized_states.append(state)
    elif prefix is None:
      assert is_input_arg  # validated by _check_out_axes
      graphdef, state = ctx.split(x)
      broadcast_states.append(state)
      vectorized_states.append(State({}))
    elif prefix is Carry:
      assert is_input_arg  # validated by _check_out_axes
      graphdef, state = ctx.split(x)
      carry_states.append(state)
      vectorized_states.append(State({}))
    else:
      obj_repr = 'args' if is_input_arg else 'out'
      raise ValueError(
        f'Invalid axes {prefix} at {obj_repr}{jax.tree_util.keystr(path)}'
      )
    if not vectorized_states:
      vectorized_states.append(State({}))
    if is_input_arg:
      carry_deque.append(carry_states)
      broadcast_deque.append(broadcast_states)
    graphdefs_deque.append(graphdef)
    return extract.NodeStates.from_split(
      None, *vectorized_states, metadata=prefix
    )
  else:
    if isinstance(prefix, StateAxes):
      obj_repr = 'args' if is_input_arg else 'out'
      raise ValueError(
        'Cannot use StateAxes on non-graph nodes, '
        f'found {prefix} at {obj_repr}{jax.tree_util.keystr(path)}'
      )
    elif prefix is Carry:
      return x
    elif prefix is None:
      assert not is_input_arg  # validated by _check_out_axes
      return Broadcasted(None)
    elif isinstance(prefix, int):
      return x
    else:
      obj_repr = 'args' if is_input_arg else 'out'
      raise ValueError(
        f'Invalid axes {prefix} at {obj_repr}{jax.tree_util.keystr(path)}'
      )

