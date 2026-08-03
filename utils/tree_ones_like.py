from typing import Any, Optional

def tree_ones_like(
    tree: Any,
    dtype: Optional[jax.typing.DTypeLike] = None,
) -> Any:
  """Creates an all-ones tree with the same structure.

  Args:
    tree: pytree.
    dtype: optional dtype to use for the tree of ones.

  Returns:
    an all-ones tree with the same structure as ``tree``.
  """
  return jax.tree.map(lambda x: jnp.ones_like(x, dtype=dtype), tree)

