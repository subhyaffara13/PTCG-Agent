
def _scan_merge_out(
  carry_deque: PytreeDeque[list[State]],
  graphdefs_deque: PytreeDeque[graphlib.GraphDef],
  broadcast_deque: PytreeDeque[list[State]],
  /,
  ctx: graphlib.MergeContext,
  path,
  prefix,
  x,
):
  assert isinstance(path[0], jax.tree_util.SequenceKey)
  is_input_arg = path[0].idx == 0

  if isinstance(x, extract.NodeStates):
    states: list[State] = []
    graphdef = graphdefs_deque.popleft()
    if is_input_arg:
      carry_states = deque(carry_deque.popleft())
      broadcast_states = deque(broadcast_deque.popleft())
    else:
      carry_states = deque[State]()
      broadcast_states = deque[State]()
    if isinstance(prefix, StateAxes):
      vectorized_states = deque(x.states)
      for axis in prefix.axes:
        if isinstance(axis, int):
          state = vectorized_states.popleft()
          state = jax.tree.map(
            lambda x: jnp.moveaxis(x, 0, axis) if axis != 0 else x,
            state,
          )
          states.append(state)
        elif axis is None:
          states.append(broadcast_states.popleft())
        else:  # axis is Carry
          states.append(carry_states.popleft())
      assert not carry_states and not broadcast_states
      assert not vectorized_states or (
        len(vectorized_states) == 1 and not vectorized_states[0]
      )
    elif isinstance(prefix, int):
      state = jax.tree.map(
        lambda x: jnp.moveaxis(x, 0, prefix) if prefix != 0 else x, x.state
      )
      states.extend((state, *carry_states, *broadcast_states))
    elif prefix is None:
      assert is_input_arg
      states.extend(broadcast_states)
    elif prefix is Carry:
      assert is_input_arg
      states.extend(carry_states)
    else:
      obj_repr = 'args' if is_input_arg else 'out'
      raise ValueError(
        f'Invalid axes {prefix} at {obj_repr}{jax.tree_util.keystr(path)}'
      )
    return ctx.merge(graphdef, *states)
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
      return x
    elif isinstance(prefix, int):
      if not isinstance(x, (jax.Array, np.ndarray)):
        obj_repr = 'args' if is_input_arg else 'out'
        raise ValueError(
          f'Expected an array, got {type(x).__name__} at '
          f'{obj_repr}{jax.tree_util.keystr(path)}'
        )
      if prefix != 0:
        x = jnp.moveaxis(x, 0, prefix)
      return x
    else:
      obj_repr = 'args' if is_input_arg else 'out'
      raise ValueError(
        f'Invalid axes {prefix} at {obj_repr}{jax.tree_util.keystr(path)}'
      )

