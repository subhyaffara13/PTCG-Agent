
def _tree_unflatten(
  graphdef: GraphDef[tp.Any],
  leaves: list[tp.Any],
  copy_variables: bool,
) -> tp.Any:
  tree_nodedef = graphdef.nodes[0]
  assert isinstance(tree_nodedef, TreeNodeDef)
  variable_defs_iter = iter(
    node for node in graphdef.nodes[1:] if isinstance(node, VariableDef)
  )
  variabledef = next(variable_defs_iter, None)

  original_leaves: list[tp.Any] = [None] * len(leaves)
  for i, (path, original_index) in enumerate(tree_nodedef.path_index):
    leaf = leaves[i]
    if variabledef is not None and variabledef.index == i:
      if isinstance(leaf, Variable):
        if copy_variables:
          leaf = leaf.copy()
      else:
        leaf = variabledef.type.from_metadata(
          leaf, dict(variabledef.metadata)
        )
      variabledef = next(variable_defs_iter, None)
    original_leaves[original_index] = leaf

  return tree_nodedef.treedef.unflatten(original_leaves)

