
def is_flat_dict(tree: PyTree) -> bool:
  """Returns True if the tree is a flat dict."""
  return isinstance(tree, dict) and all(is_leaf_node(v) for v in tree.values())

