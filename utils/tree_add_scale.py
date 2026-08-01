
def tree_add_scale(
    tree_x: Any, scalar: jax.typing.ArrayLike, tree_y: Any
) -> Any:
  r"""Add two trees, where the second tree is scaled by a scalar.

  In infix notation, the function performs ``out = tree_x + scalar * tree_y``.

  Args:
    tree_x: first pytree.
    scalar: scalar value.
    tree_y: second pytree.

  Returns:
    a pytree with the same structure as ``tree_x`` and ``tree_y``.
  """
  scalar = jnp.asarray(scalar)
  return jax.tree.map(
      lambda x, y: (None if x is None else (x + scalar * y)),
      tree_x, tree_y, is_leaf=lambda x: x is None)

