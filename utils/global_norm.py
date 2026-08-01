
def global_norm(updates: base.PyTree) -> jax.Array:
  """Compute the global norm across a nested structure of tensors.

  .. warning::
    Deprecated in favor of :func:`optax.tree.norm`.
  Args:
    updates: A nested structure of tensors.
  Returns:
    The global L2 norm of the updates.
  """
  warnings.warn(
      'optax.global_norm is deprecated in favor of optax.tree.norm',
      DeprecationWarning
  )
  return optax.tree.norm(updates)

