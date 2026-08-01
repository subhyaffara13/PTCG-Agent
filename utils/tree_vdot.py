
def tree_vdot(tree_x: Any, tree_y: Any) -> jax.typing.ArrayLike:
  r"""Compute the inner product between two pytrees.

  Args:
    tree_x: first pytree to use.
    tree_y: second pytree to use.

  Returns:
    inner product between ``tree_x`` and ``tree_y``, a scalar value.

  Examples:

    >>> optax.tree_utils.tree_vdot(
    ...   {'a': jnp.array([1, 2]), 'b': jnp.array([1, 2])},
    ...   {'a': jnp.array([-1, -1]), 'b': jnp.array([1, 1])},
    ... )
    Array(0, dtype=int32)

  .. note::
    We upcast the values to the highest precision to avoid
    numerical issues.
  """
  vdots = jax.tree.map(_vdot_safe, tree_x, tree_y)
  return jax.tree.reduce(operator.add, vdots, initializer=0)

