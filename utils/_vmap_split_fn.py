
def _vmap_split_fn(ctx: graphlib.SplitContext, path, prefix, x):
  if isinstance(prefix, StateAxes):
    return extract.NodeStates.from_split(
      *ctx.split(x, *prefix.filters), metadata=prefix
    )
  return extract.NodeStates.from_split(*ctx.split(x), metadata=prefix)

