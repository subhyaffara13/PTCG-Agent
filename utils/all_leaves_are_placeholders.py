
def all_leaves_are_placeholders(tree: PyTree) -> bool:
  """Determines if all leaves in `tree` are placeholders."""
  return all(leaf_is_placeholder(leaf) for leaf in jax.tree.leaves(tree))

