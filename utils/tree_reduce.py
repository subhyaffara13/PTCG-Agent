import functools
from typing import Any, Callable

def tree_reduce(function: Callable[[T, Any], T],
                tree: Any,
                initializer: T | Unspecified = Unspecified(),
                is_leaf: Callable[[Any], bool] | None = None) -> T:
  """Alias of :func:`jax.tree.reduce`."""
  if isinstance(initializer, Unspecified):
    return functools.reduce(function, tree_leaves(tree, is_leaf=is_leaf))
  else:
    return functools.reduce(function, tree_leaves(tree, is_leaf=is_leaf), initializer)

