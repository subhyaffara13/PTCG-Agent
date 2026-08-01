
def copy_to_host_async(x):
  """
  Tries to call a ``copy_to_host_async`` method on pytree leaves.

  For each leaf this method will try to call the ``copy_to_host_async`` method
  on the leaf. If the leaf is not a JAX array, or if the leaf does not have a
  ``copy_to_host_async`` method, then this method will do nothing to the leaf.

  Args:
    x: a pytree, usually with at least some JAX array instances at its leaves.

  Returns:
    A pytree with the same structure and values of the input, where the host
    copy of the values of all JAX array leaves are started.
  """
  for leaf in tree_leaves(x):
    try:
      copy_fn = leaf.copy_to_host_async
    except AttributeError:
      pass
    else:
      copy_fn()

  return x

