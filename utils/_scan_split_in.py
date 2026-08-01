
def _scan_split_in(
  carry_deque: PytreeDeque[list[State | variablelib.Variable]],
  graphdefs_deque: PytreeDeque[graphlib.GraphDef],
  broadcast_deque: PytreeDeque[list[State | variablelib.Variable]],
  broadcast_arrays: PytreeDeque[Broadcasted],
  /,
  ctx: graphlib.SplitContext,
  path,
  prefix,
  x,
):
  if graphlib.is_graph_node(x) or isinstance(x, variablelib.Variable):
    vectorized_states: list[State | variablelib.Variable] = []
    carry_states: list[State | variablelib.Variable] = []
    broadcast_states: list[State | variablelib.Variable] = []
    if isinstance(prefix, StateAxes):
      graphdef, *states = ctx.split(x, *prefix.filters)

      for state, axis in zip(states, prefix.axes):
        if axis is None:
          broadcast_states.append(state)
        elif isinstance(axis, int):
          if axis != 0:
            state = jax.tree.map(lambda x: jnp.moveaxis(x, axis, 0), state)
          vectorized_states.append(state)
        else:  # axis is Carry
          carry_states.append(state)
      if not vectorized_states:
        vectorized_states.append(State({}))
      carry_deque.append(carry_states)
      graphdefs_deque.append(graphdef)
      broadcast_deque.append(broadcast_states)
      return extract.NodeStates.from_split(
        None, *vectorized_states, metadata=prefix
      )
    elif isinstance(prefix, int):
      graphdef, state = ctx.split(x)
      if prefix != 0:
        state = jax.tree.map(lambda x: jnp.moveaxis(x, prefix, 0), state)
      vectorized_states.append(state)
    elif prefix is None:
      graphdef, state = ctx.split(x)
      broadcast_states.append(state)
      vectorized_states.append(State({}))
    elif prefix is Carry:
      graphdef, state = ctx.split(x)
      carry_states.append(state)
      vectorized_states.append(State({}))
    else:
      raise ValueError(
        f'Invalid axes {prefix} args{jax.tree_util.keystr(path)}'
      )

    if not vectorized_states:
      vectorized_states.append(State({}))
    carry_deque.append(carry_states)
    graphdefs_deque.append(graphdef)
    broadcast_deque.append(broadcast_states)
    return extract.NodeStates.from_split(
      None, *vectorized_states, metadata=prefix
    )
  else:
    if isinstance(prefix, StateAxes):
      raise ValueError(
        'Cannot use StateAxes on non-graph nodes, '
        f'found {prefix} args{jax.tree_util.keystr(path)}'
      )
    elif prefix is Carry:
      return x
    elif prefix is None:
      broadcast_arrays.append(Broadcasted(x))
      return Broadcasted(None)
    elif isinstance(prefix, int):
      if not isinstance(x, (jax.Array, np.ndarray)):
        raise ValueError(
          f'Expected an array, got {type(x).__name__} args'
          f'{jax.tree_util.keystr(path)}'
        )
      if prefix != 0:
        x = jnp.moveaxis(x, prefix, 0)
      return x
    else:
      raise ValueError(
        f'Invalid axes {prefix} args{jax.tree_util.keystr(path)}'
      )

