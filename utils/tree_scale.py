
def tree_scale(
    scalar: jax.typing.ArrayLike,
    tree: Any,
) -> Any:
  r"""Multiply a tree by a scalar.

  In infix notation, the function performs ``out = scalar * tree``.

  Args:
    scalar: scalar value.
    tree: pytree.

  Returns:
    a pytree with the same structure as ``tree``.
  """
  return jax.tree.map(lambda x: scalar * x, tree)

