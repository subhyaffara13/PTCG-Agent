from typing import Any

def tree_sum(
    tree: Any, associative_reduction: bool = False
) -> jax.typing.ArrayLike:
  """Compute the sum of all the elements in a pytree.

  Args:
    tree: pytree.
    associative_reduction: If True, use reduce_associative for a potential
      compilation time speedup with large pytrees (requires JAX >= 0.6.0).
      This changes the order of summation which may result in slightly
      different floating-point values. Default is False.

  Returns:
    a scalar value.
  """
  sums = jax.tree.map(jnp.sum, tree)
  if associative_reduction:
    # Use reduce_associative for a potential compilation time speedup
    if hasattr(jax.tree, 'reduce_associative'):
      return jax.tree.reduce_associative(operator.add, sums, identity=0)
    else:
      raise ValueError(
          'associative_reduction=True requires JAX >= 0.6.0 which provides '
          'tree.reduce_associative. Please upgrade JAX or use '
          'associative_reduction=False.'
      )
  else:
    return jax.tree.reduce(operator.add, sums, initializer=0)

