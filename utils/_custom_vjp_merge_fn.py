
def _custom_vjp_merge_fn(
  ctx: graphlib.MergeContext,
  path,
  prefix: bool | DiffState,
  value: extract.NodeStates,
  *,
  nondiff_states: deque[extract.GraphDefState],
):
  nondiff = nondiff_states.popleft()
  return ctx.merge(nondiff.graphdef, value.state, nondiff.state)

