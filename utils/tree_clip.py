from typing import Any, Optional

def tree_clip(
    tree: Any,
    min_value: Optional[jax.typing.ArrayLike] = None,
    max_value: Optional[jax.typing.ArrayLike] = None,
) -> Any:
  """Creates an identical tree where all tensors are clipped to `[min, max]`.

  Args:
    tree: pytree.
    min_value: optional minimal value to clip all tensors to. If ``None``
      (default) then result will not be clipped to any minimum value.
    max_value: optional maximal value to clip all tensors to. If ``None``
      (default) then result will not be clipped to any maximum value.

  Returns:
    a tree with the same structure as ``tree``.

  .. versionadded:: 0.2.3
  """
  return jax.tree.map(lambda g: jnp.clip(g, min_value, max_value), tree)

