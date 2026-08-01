
def setup_pytree(add: int = 0):
  """Creates a numpy PyTree for testing."""
  pytree = {
      'a': np.arange(8) * 1,
      'b': np.arange(16) * 2,
      'c': {
          'a': np.arange(8).reshape((2, 4)) * 3,
          'e': np.arange(16).reshape((4, 4)) * 4,
      },
  }
  pytree = jax.tree.map(lambda x: x + add, pytree, is_leaf=is_leaf)
  return pytree

