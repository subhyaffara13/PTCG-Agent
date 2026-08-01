
def _scan_merge_in(
  carry_deque: PytreeDeque[list[State]],
  graphdefs_deque: PytreeDeque[graphlib.GraphDef],
  broadcast_deque: PytreeDeque[list[State]],
  broadcast_arrays: PytreeDeque[Broadcasted],
  /,
  ctx: graphlib.MergeContext,
  path,
  prefix,
  x,
):
  if isinstance(x, extract.NodeStates):
    carry_states = carry_deque.popleft()
    broadcast_states = broadcast_deque.popleft()
    graphdef = graphdefs_deque.popleft()
    return ctx.merge(graphdef, *x.states, *carry_states, *broadcast_states)
  elif isinstance(x, Broadcasted):
    assert x.data is None
    return broadcast_arrays.popleft().data
  else:
    return x

