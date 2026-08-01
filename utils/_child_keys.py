
def _child_keys(pytree: Any) -> KeyPath:
  assert not treedef_is_strict_leaf(tree_structure(pytree))
  return tuple(k for k, _ in flatten_one_level_with_keys(pytree)[0])

