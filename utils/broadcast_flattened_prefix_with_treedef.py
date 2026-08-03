from typing import Any

def broadcast_flattened_prefix_with_treedef(
    prefix_leaves: list[Any],
    prefix_treedef: PyTreeDef,
    full_treedef: PyTreeDef,
) -> list[Any]:
  """Broadcasts tree prefix leaves into the full set of leaves for a given full treedef.

    Args:
      prefix_leaves: the leaves of a pytree that is a tree prefix
        of full_treedef.
      prefix_treedef: the PyTreeDef of a pytree that is a tree prefix of
        full_treedef.
      full_treedef: a PyTreeDef with the structure to broadcast the prefix
        leaves into.

    Returns:
      A list of leaves matching the expected count for the full tree,
      with each leaf of prefix tree being duplicated to match the count of
      its corresponding subtree.
  """
  # NOTE: At the moment, `broadcast_flattened_prefix_with_treedef` is only
  # called from `api_util.flatten_axes`, which replaces any raised exception
  # with its own exception and error message.  The errors raised from this
  # function should probably be improved before this function is used in
  # more places.
  #
  # TODO(jburnim): Merge `broadcast_prefix` with this function?
  # prefix_leaves, prefix_treedef = tree_flatten(prefix_tree, is_leaf)
  ret = []

  # TODO(jburnim): Should this traversal be done in C++?
  def _broadcast(broadcast_fn, leaf_start, leaf_end, prefix_treedef, treedef):
    if treedef_is_strict_leaf(prefix_treedef):
      # We have encountered a leaf in the prefix, so we repeat the prefix leaf
      # for each leaf in the corresponding part of the tree.
      assert (leaf_end - leaf_start) == 1
      ret.extend(prefix_leaves[leaf_start:leaf_end] * treedef.num_leaves)
      return

    if treedef_is_strict_leaf(treedef):
      raise ValueError('`prefix_treedef` is not a prefix of `full_treedef`')

    prefix_node_data = prefix_treedef.node_data()
    node_data = treedef.node_data()
    if prefix_node_data != node_data:
      raise ValueError(f'expected {node_data}, got {prefix_node_data}')

    prefix_i = leaf_start
    for prefix_child, tree_child in zip(
        prefix_treedef.children(), treedef.children(), strict=True):
      broadcast_fn(broadcast_fn, prefix_i, prefix_i + prefix_child.num_leaves,
                   prefix_child, tree_child,
      )
      prefix_i += prefix_child.num_leaves

  # Pass _broadcast as arg to avoid it being a free variable within its own
  # closure, which creates a reference cycle.
  _broadcast(_broadcast, 0, len(prefix_leaves), prefix_treedef, full_treedef)
  return ret

