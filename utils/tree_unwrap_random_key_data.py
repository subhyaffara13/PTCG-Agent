
def tree_unwrap_random_key_data(input_tree: base.ArrayTree) -> base.ArrayTree:
  """Unwrap random.key objects in a tree for numerical comparison.

  Args:
    input_tree: a tree of arrays and random.key objects.

  Returns:
    a tree of arrays and random.key_data objects.
  """
  def _unwrap_random_key_data(x):
    if (isinstance(x, jax.Array)
        and jax.dtypes.issubdtype(x.dtype, jax.dtypes.prng_key)):
      return jax.random.key_data(x)
    return x

  return jax.tree.map(_unwrap_random_key_data, input_tree)

