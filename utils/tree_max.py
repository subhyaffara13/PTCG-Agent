from typing import Any

def tree_max(tree: Any) -> jax.typing.ArrayLike:
  """Compute the max of all the elements in a pytree.

  Args:
    tree: pytree.

  Returns:
    a scalar value.
  """
  def f(array):
    if jnp.size(array) == 0:
      return None
    else:
      return jnp.max(array)
  maxes = jax.tree.map(f, tree)
  return jax.tree.reduce(jnp.maximum, maxes, initializer=-float('inf'))

