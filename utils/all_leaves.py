from typing import Any, Callable

def all_leaves(iterable: Iterable[Any],
               is_leaf: Callable[[Any], bool] | None = None) -> bool:
  """Tests whether all elements in the given iterable are all leaves.

  This function is useful in advanced cases, for example if a library allows
  arbitrary map operations on a flat iterable of leaves it may want to check
  if the result is still a flat iterable of leaves.

  Args:
    iterable: Iterable of leaves.

  Returns:
    A boolean indicating if all elements in the input are leaves.

  Examples:
    >>> import jax
    >>> tree = {"a": [1, 2, 3]}
    >>> assert all_leaves(jax.tree_util.tree_leaves(tree))
    >>> assert not all_leaves([tree])
  """
  if is_leaf is None:
    return pytree.all_leaves(default_registry, iterable)
  else:
    items = list(iterable)
    leaves = tree_leaves(items, is_leaf)
    return len(leaves) == len(items) and all(
        item is leaf for item, leaf in zip(items, leaves, strict=True)
    )

