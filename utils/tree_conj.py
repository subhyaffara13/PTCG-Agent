
def tree_conj(tree: Any) -> Any:
  """Compute the conjugate of a pytree.

  Args:
    tree: pytree.

  Returns:
    a pytree with the same structure as ``tree``.
  """
  return jax.tree.map(jnp.conj, tree)

