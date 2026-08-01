
def treedef_is_strict_leaf(treedef: PyTreeDef) -> bool:
  return treedef.num_nodes == 1 and treedef.num_leaves == 1

