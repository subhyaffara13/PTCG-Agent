
def tree_leaves_checked(treedef_expected: PyTreeDef, tree: Any) -> list[Leaf]:
  flat_vals, treedef_actual = tracing_registry.flatten(tree)
  assert treedef_actual == treedef_expected
  return flat_vals

