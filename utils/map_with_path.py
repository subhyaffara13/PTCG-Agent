from typing import Any, Callable

def map_with_path(
    f: Callable[..., Any],
    tree: Any,
    *rest: Any,
    is_leaf: Callable[..., bool] | None = None,
    is_leaf_takes_path: bool = False,
) -> Any:
  """Maps a multi-input function over pytree key path and args to produce a new pytree.

  This is a more powerful alternative of ``tree_map`` that can take the key path
  of each leaf as input argument as well.

  Args:
    f: function that takes ``2 + len(rest)`` arguments, aka. the key path and
      each corresponding leaves of the pytrees.
    tree: a pytree to be mapped over, with each leaf's key path as the first
      positional argument and the leaf itself as the second argument to ``f``.
    *rest: a tuple of pytrees, each of which has the same structure as ``tree``
      or has ``tree`` as a prefix.

  Returns:
    A new pytree with the same structure as ``tree`` but with the value at each
    leaf given by ``f(kp, x, *xs)`` where ``kp`` is the key path of the leaf at
    the corresponding leaf in ``tree``, ``x`` is the leaf value and ``xs`` is
    the tuple of values at corresponding nodes in ``rest``.

  Examples:
    >>> import jax
    >>> jax.tree.map_with_path(lambda path, x: x + path[0].idx, [1, 2, 3])
    [1, 3, 5]

  See Also:
    - :func:`jax.tree.map`
    - :func:`jax.tree.flatten_with_path`
    - :func:`jax.tree.leaves_with_path`
    - :func:`jax.tree_util.register_pytree_with_keys`
  """
  return tree_util.tree_map_with_path(
      f, tree, *rest, is_leaf=is_leaf, is_leaf_takes_path=is_leaf_takes_path
  )

