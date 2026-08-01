
def clear_pytree(pytree: Any) -> Any:
  """Clears the pytree to free up memory."""
  return jax.tree.map(
      lambda x: x.delete() if isinstance(x, jax.Array) else None, pytree
  )

