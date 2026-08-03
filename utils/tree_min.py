from typing import Any

def tree_min(tree: Any) -> jax.typing.ArrayLike:
  """Compute the min of all the elements in a pytree.

  Args:
    tree: pytree.

  Returns:
    a scalar value.
  """
  def f(array):
    if jnp.size(array) == 0:
      return None
    else:
      return jnp.min(array)
  mins = jax.tree.map(f, tree)
  return jax.tree.reduce(jnp.minimum, mins, initializer=float('inf'))

