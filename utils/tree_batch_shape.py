
def tree_batch_shape(
    tree: Any,
    shape: tuple[int, ...] = (),
):
  """Add leading batch dimensions to each leaf of a pytree.

  Args:
    tree: a pytree.
    shape: a shape indicating what leading batch dimensions to add.

  Returns:
    a pytree with the leading batch dimensions added.
  """
  return jax.tree.map(
      lambda x: jnp.broadcast_to(x, (*shape, *jnp.shape(x))), tree
  )

