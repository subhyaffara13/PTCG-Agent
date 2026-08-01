
def default_split_fn(
  ctx: graphlib.SplitContext, path: KeyPath, prefix: Prefix, leaf: Leaf
) -> tp.Any:
  return NodeStates.from_split(*ctx.split(leaf))

