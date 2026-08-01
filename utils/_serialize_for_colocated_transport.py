
def _serialize_for_colocated_transport(tree: PyTree) -> PyTree:
  """Canonicalizes a PyTree before it crosses the colocated boundary."""
  return tree_metadata.serialize_tree(
      tree, tree_metadata.PYTREE_METADATA_OPTIONS
  )

