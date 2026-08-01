
def _check_arrays_have_batch_dim(grads: base.ArrayTree) -> bool:
  """Checks that each array in grads has a batch dimension in the 0th axis."""
  grads = jax.tree.flatten(grads)[0]
  batch_size = grads[0].shape[0]
  return all(g.ndim >= 1 and batch_size == g.shape[0] for g in grads)

