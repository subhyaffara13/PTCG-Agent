
def merge_tree_node(
  ctx: graphlib.MergeContext, path: KeyPath, prefix: Prefix, leaf: Leaf
) -> tp.Any:
  if not isinstance(leaf, NodeStates):
    raise ValueError(f'Expected TreeNode, got {type(leaf)} at path {path}')
  return ctx.merge(leaf.graphdef, *leaf.states)

