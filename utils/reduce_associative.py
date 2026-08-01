
def reduce_associative(
    operation: Callable[[T, T], T],
    tree: Any,
    *,
    identity: T | tree_util.Unspecified = tree_util.Unspecified(),
    is_leaf: Callable[[Any], bool] | None = None,
) -> T:
  """Perform a reduction over a pytree with an associative binary operation.

  This function exploits the fact that the operation is associative to perform
  the reduction in parallel (logarithmic depth).

  Args:
    operation: the associative binary operation
    tree: the pytree to reduce
    identity: the identity element of the associative binary operation.
      This is used only when the tree is empty. It is optional otherwise.
    is_leaf: an optionally specified function that will be called at each
      flattening step. It should return a boolean, which indicates whether the
      flattening should traverse the current object, or if it should be stopped
      immediately, with the whole subtree being treated as a leaf.

  Returns:
    result: the reduced value

  Examples:
    >>> import jax
    >>> import operator
    >>> jax.tree.reduce_associative(operator.add, [1, (2, 3), [4, 5, 6]])
    21

  Notes:
    **Tip**: You can exclude leaves from the reduction by first mapping them to
    ``None`` using :func:`jax.tree.map`. This causes them to not be counted as
    leaves after that.

  See Also:
    - :func:`jax.tree.reduce`
  """
  return tree_util.tree_reduce_associative(
      operation,
      tree,
      identity=identity,
      is_leaf=is_leaf,
  )

