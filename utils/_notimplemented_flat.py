
def _notimplemented_flat(self):
  """Not implemented: Use :meth:`~jax.Array.flatten` instead."""
  raise NotImplementedError("JAX Arrays do not implement the arr.flat property: "
                            "consider arr.flatten() instead.")

