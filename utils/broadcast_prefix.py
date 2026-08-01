
def broadcast_prefix(
    prefix_tree: PyTree,
    full_tree: PyTree,
    is_leaf: Callable[[PyTree], bool] | None = None,
) -> list[Any]:
    """Return a list of broadcasted leaves in ``prefix_tree`` to match the number of leaves in ``full_tree``.

    If a ``prefix_tree`` is a prefix of a ``full_tree``, this means the ``full_tree`` can be
    constructed by replacing the leaves of ``prefix_tree`` with appropriate **subtrees**.

    This function returns a list of leaves with the same size as ``full_tree``. The leaves are
    replicated from ``prefix_tree``. The number of replicas is determined by the corresponding
    subtree in ``full_tree``.

    >>> broadcast_prefix(1, [1, 2, 3])
    [1, 1, 1]
    >>> broadcast_prefix([1, 2, 3], [1, 2, 3])
    [1, 2, 3]
    >>> broadcast_prefix([1, 2, 3], [1, 2, 3, 4])
    Traceback (most recent call last):
        ...
    ValueError: list arity mismatch; expected: 3, got: 4; list: [1, 2, 3, 4].
    >>> broadcast_prefix([1, 2, 3], [1, 2, (3, 4)])
    [1, 2, 3, 3]
    >>> broadcast_prefix([1, 2, 3], [1, 2, {"a": 3, "b": 4, "c": (None, 5)}])
    [1, 2, 3, 3, 3, 3]

    Args:
        prefix_tree (pytree): A pytree with the same structure as a prefix of ``full_tree``.
        full_tree (pytree): A pytree with the same structure as a suffix of ``prefix_tree``.
        is_leaf (callable, optional): An extra leaf predicate function that will be called at each
            flattening step. The function should have a single argument with signature
            ``is_leaf(node) -> bool``. If it returns :data:`True`, the whole subtree being treated
            as a leaf. Otherwise, the default pytree registry will be used to determine a node is a
            leaf or not. If the function is not specified, the default pytree registry will be used.

    Returns:
        A list of leaves in ``prefix_tree`` broadcasted to match the number of leaves in ``full_tree``.
    """
    result: list[Any] = []

    def add_leaves(x: Any, subtree: PyTree) -> None:
        subtreespec = tree_structure(subtree, is_leaf=is_leaf)
        result.extend([x] * subtreespec.num_leaves)

    tree_map_(
        add_leaves,
        prefix_tree,
        full_tree,
        is_leaf=is_leaf,
    )
    return result


def broadcast_prefix(prefix_tree: Any, full_tree: Any,
                     is_leaf: Callable[[Any], bool] | None = None
                     ) -> list[Any]:
  """Broadcasts tree prefix leaves into the full set of leaves for a given full tree.

    Args:
      prefix_tree: a pytree that is a tree prefix of full_tree.
      full_tree: a pytree with the structure to broadcast the prefix leaves into.
      is_leaf: an optionally specified function that will be called at each
        flattening step for prefix_tree. It should return a boolean, with true
        stopping the traversal and the whole subtree being treated as a leaf,
        and false indicating the flattening should traverse the current object.

    Returns:
      A list of leaves matching the expected count for the full tree,
      with the leaf of each prefix tree being duplicated to match the count of
      its corresponding subtree.
  """
  result = []
  num_leaves = lambda t: tree_structure(t).num_leaves
  add_leaves = lambda x, subtree: result.extend([x] * num_leaves(subtree))
  try:
    tree_map(add_leaves, prefix_tree, full_tree, is_leaf=is_leaf)
  except ValueError:
      e, *_ = prefix_errors(prefix_tree, full_tree)
      raise e('broadcast_prefix prefix_tree') from None
  return result


def broadcast_prefix(
  prefix_tree: tp.Any,
  full_tree: tp.Any,
  prefix_is_leaf: tp.Callable[[tp.Any], bool] | None = None,
  tree_is_leaf: tp.Callable[[tp.Any], bool] | None = None,
) -> list[tp.Any]:
  # If prefix_tree is not a tree prefix of full_tree, this code can raise a
  # ValueError; use prefix_errors to find disagreements and raise more precise
  # error messages.
  result = []
  num_leaves = lambda t: jax.tree_util.tree_structure(
    t, is_leaf=tree_is_leaf
  ).num_leaves
  add_leaves = lambda x, subtree: result.extend([x] * num_leaves(subtree))
  jax.tree.map(
    add_leaves,
    prefix_tree,
    full_tree,
    is_leaf=lambda x: isinstance(x, variablelib.Variable)
    or graphlib.is_graph_node(x)
    or (prefix_is_leaf is not None and prefix_is_leaf(x)),
  )
  return result

