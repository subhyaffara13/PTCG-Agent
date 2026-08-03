from typing import Any, Optional

def tree_zeros_like(
    tree: Any,
    dtype: Optional[jax.typing.DTypeLike] = None,
) -> Any:
  """Creates an all-zeros tree with the same structure.

  Args:
    tree: pytree.
    dtype: optional dtype to use for the tree of zeros.

  Returns:
    an all-zeros tree with the same structure as ``tree``.
  """
  return jax.tree.map(lambda x: jnp.zeros_like(x, dtype=dtype), tree)

