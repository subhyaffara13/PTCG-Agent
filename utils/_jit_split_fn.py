
def _jit_split_fn(ctx: graphlib.SplitContext, path, prefix, x):
  if isinstance(prefix, StateSharding):
    graphdef, *states = ctx.flatten(x, *prefix.filters)
    return extract.NodeStates.from_split(graphdef, *states, metadata=prefix)
  return extract.NodeStates.from_split(*ctx.flatten(x, with_paths=False))

