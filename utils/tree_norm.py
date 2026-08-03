from typing import Any

def tree_norm(tree: Any,
              ord: int | str | float | None = None,  # pylint: disable=redefined-builtin
              squared: bool = False) -> jax.Array:
  """Compute the vector norm of the given ord of a pytree.

  Args:
    tree: pytree.
    ord: the order of the vector norm to compute from (None, 1, 2, inf).
    squared: whether the norm should be returned squared or not.

  Returns:
    a scalar value.
  """
  if ord is None or ord == 2:
    squared_tree = jax.tree.map(_square, tree)
    sqnorm = tree_sum(squared_tree)
    return jnp.array(sqnorm if squared else jnp.sqrt(sqnorm))
  elif ord == 1:
    ret = tree_sum(jax.tree.map(jnp.abs, tree))
  elif ord == jnp.inf or ord in ('inf', 'infinity'):
    ret = tree_max(jax.tree.map(jnp.abs, tree))
  else:
    raise ValueError(f'Unsupported ord: {ord}')
  return jnp.array(ret if not squared else _square(ret))

