
def _is_locally_available(array: jax.Array) -> bool:
  """Checks if the array is available locally."""
  return getattr(array, "is_fully_addressable", False) or getattr(
      array, "is_fully_replicated", False
  )

