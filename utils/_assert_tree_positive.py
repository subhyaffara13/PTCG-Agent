
def _assert_tree_positive(tree):
  # Use jnp instead of np for testing purposes.
  if not all((x > 0).all() for x in jax.tree_util.tree_leaves(tree)):
    raise AssertionError('Tree contains non-positive elems!')

