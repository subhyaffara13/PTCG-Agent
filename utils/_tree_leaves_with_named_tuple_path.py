
def _tree_leaves_with_named_tuple_path(
    tree: base.PyTree,
    is_leaf: Optional[
        Callable[
            [
                Any,
            ],
            bool,
        ]
    ] = None,
) -> list[tuple[_KeyPath, Any]]:
  """Get leaves of a tree with their path.

  Essentially the same as :func:`jax.tree_util.tree_leaves_with_path`.
  The difference is that for each attribute of a named tuple we add to the given
  entry the name of the tuple. This facilitates getting/setting values in a
  pytree by filtering for attributes in specific states (different named tuples)
  that have otherwise the same name and type.
  See :func:`optax.tree_utils.tree_get` for a concrete example.

  Args:
    tree: pytree to extract leaves of.
    is_leaf: callable to stop expanding the tree at a node that satisfies
      is_leaf(node) == True.

  Returns:
    list of (path_to_leaf, leaf) for all leaves in the tree
    (or nodes satisfying is_leaf(node) == True).
  """
  is_leaf_ = is_leaf if is_leaf else lambda _: False
  tree_leaves_with_path = jax.tree_util.tree_leaves_with_path(
      tree, is_leaf=lambda x: is_leaf_(x) or _is_named_tuple(x)
  )
  named_tree_leaves_with_path = []
  for path, node in tree_leaves_with_path:
    if is_leaf_(node) or not _is_named_tuple(node):
      named_tree_leaves_with_path.append((path, node))
    else:
      for field in node._fields:
        child_leaves_with_path = _tree_leaves_with_named_tuple_path(
            getattr(node, field), is_leaf
        )
        child_leaves_with_path = [
            (
                (
                    *path,
                    NamedTupleKey(node.__class__.__name__, field),
                    *child_path,
                ),
                child_value,
            )
            for child_path, child_value in child_leaves_with_path
        ]
        named_tree_leaves_with_path = (
            named_tree_leaves_with_path + child_leaves_with_path
        )
  return named_tree_leaves_with_path

