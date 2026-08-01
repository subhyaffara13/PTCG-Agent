
def block_until_ready(x):
  """
  Tries to call a ``block_until_ready`` method on pytree leaves.

  Args:
    x: a pytree, usually with at least some JAX array instances at its leaves.

  Returns:
    A pytree with the same structure and values of the input, where the values
    of all JAX array leaves are ready.
  """
  def try_to_block(x):
    try:
      return x.block_until_ready()
    except AttributeError:
      return x

  arrays = []
  for leaf in tree_leaves(x):
    if isinstance(leaf, array.ArrayImpl):
      arrays.append(leaf)
    else:
      try_to_block(leaf)

  if not arrays:
    # `arrays` will be empty if tree_leaves(x) is empty or all leaves are not
    # jax.Array.
    pass
  elif len(arrays) == 1:
    # Fast path for single array.
    try_to_block(arrays[0])
  else:
    # Optimized for multiple arrays.
    xc.batched_block_until_ready(arrays)

  return x

