
def _jit_merge_fn(ctx: graphlib.MergeContext, path, prefix, leaf) -> tp.Any:
  if not isinstance(leaf, extract.NodeStates):
    raise ValueError(f'Expected TreeNode, got {type(leaf)} at path {path}')
  return ctx.unflatten(leaf.graphdef, *leaf.states)

