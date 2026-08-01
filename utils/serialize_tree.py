
def serialize_tree(
    tree: PyTree,
    pytree_metadata_options: PyTreeMetadataOptions,
) -> PyTree:
  """Transforms a PyTree to a serializable format.

  IMPORTANT: If `pytree_metadata_options.support_rich_types` is false, the
  returned tree replaces tuple container nodes with list nodes.

  IMPORTANT: If `pytree_metadata_options.support_rich_types` is false, the
  returned tree replaces NamedTuple container nodes with dict
  nodes.

  If `pytree_metadata_options.support_rich_types` is true, then the returned
  tree is the same as the input tree retaining empty nodes as leafs.

  Args:
    tree: The tree to serialize.
    pytree_metadata_options: `PyTreeMetadataOptions` for managing PyTree
      metadata.

  Returns:
    The serialized PyTree.
  """
  if pytree_metadata_options.support_rich_types:
    return jax.tree_util.tree_map(
        lambda x: x,
        tree,
        is_leaf=tree_utils.is_empty_or_leaf,
    )

  return tree_utils.serialize_tree(tree, keep_empty_nodes=True)


def serialize_tree(tree: PyTree, keep_empty_nodes: bool = False) -> PyTree:
  """Transforms a PyTree to a serializable format.

  IMPORTANT: The returned tree replaces tuple container nodes with list nodes.

  IMPORTANT: The returned tree replaces NamedTuple container nodes with dict
  nodes.


  Args:
    tree: The tree to serialize, if tree is empty and keep_empty_nodes is False,
      an error is raised as there is no valid representation.
    keep_empty_nodes: If true, does not filter out empty nodes.

  Returns:
    The serialized PyTree.
  """
  flat_with_keys, _ = jax.tree_util.tree_flatten_with_path(
      tree, is_leaf=is_empty_or_leaf if keep_empty_nodes else None
  )
  return from_flattened_with_keypath(flat_with_keys)

