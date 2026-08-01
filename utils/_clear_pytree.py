
def _clear_pytree(pytree: Any) -> None:
  """Frees the device arrays held by a pytree."""
  jax.tree.map(
      lambda x: x.delete() if isinstance(x, jax.Array) else None, pytree
  )

