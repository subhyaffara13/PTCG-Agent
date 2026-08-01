
def _custom_vjp_split_fn(
  ctx: graphlib.SplitContext,
  path,
  prefix: bool | DiffState,
  value,
  *,
  nondiff_states: list[extract.GraphDefState],
):
  broadcast: State
  if prefix is False:
    # pure non-differentiable arg, not supported
    raise TypeError(
      'Passing integers to nondiff_argnums for graph nodes arguments in custom_vjp is not supported. '
      f'Got {prefix} at path {jax.tree_util.keystr(path)} for value {value}'
    )
  elif prefix is True:
    # pure differentiable arg, we pass all the state through
    # but we return a TreeNode.from_states which doesn't have a graphdef
    # in order to keep the gradients clean from any metadata
    graphdef, passed = ctx.split(value)
    broadcast = State({})
    nondiff_states.append(extract.GraphDefState(graphdef, broadcast))
    return extract.NodeStates.from_states(passed)
  else:
    # differentiable arg with DiffState filter, we use the filter to split the state
    # as before we return a TreeNode.from_states to keep the gradients clean
    # from any metadata, the non-differentiable state is stored in a deque
    # which is broadcasted during the forward pass
    graphdef, passed, broadcast = ctx.split(value, prefix.filter, ...)  # type: ignore[misc]
    nondiff_states.append(extract.GraphDefState(graphdef, broadcast))
    return extract.NodeStates.from_states(passed)


  nondiff_argnums: tuple[int, ...] = struct.field(pytree_node=False)
  tangent_tree_node_args: tuple[tp.Any, ...] = struct.field(pytree_node=False)

