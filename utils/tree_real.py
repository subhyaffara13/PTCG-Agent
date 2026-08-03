from typing import Any

def tree_real(tree: Any) -> Any:
  """Compute the real part of a pytree.

  Args:
    tree: pytree.

  Returns:
    a pytree with the same structure as ``tree``.
  """
  return jax.tree.map(jnp.real, tree)

