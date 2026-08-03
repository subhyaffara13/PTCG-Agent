from typing import Any, Optional

def tree_full_like(
    tree: Any,
    fill_value: jax.typing.ArrayLike,
    dtype: Optional[jax.typing.DTypeLike] = None,
) -> Any:
  """Creates an identical tree where all tensors are filled with ``fill_value``.

  Args:
    tree: pytree.
    fill_value: the fill value for all tensors in the tree.
    dtype: optional dtype to use for the tensors in the tree.

  Returns:
    an tree with the same structure as ``tree``.
  """
  return jax.tree.map(lambda x: jnp.full_like(x, fill_value, dtype=dtype), tree)

