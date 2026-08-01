
def tree_cast_like(tree: T, other_tree: base.ArrayTree) -> T:
  """Cast tree to dtypes of other_tree.

  Args:
    tree: the tree to cast.
    other_tree: reference array tree to use to cast to dtypes of leaves

  Returns:
    the tree, with leaves cast to dtype.

  Examples:
    >>> import jax.numpy as jnp
    >>> import optax
    >>> tree = {'a': {'b': jnp.array(1.0, dtype=jnp.float32)},
    ...         'c': jnp.array(2.0, dtype=jnp.float32)}
    >>> other_tree = {'a': {'b': jnp.array(1.0, dtype=jnp.float32)},
    ...               'c': jnp.array(2.0, dtype=jnp.bfloat16)}
    >>> optax.tree_utils.tree_cast_like(tree, other_tree)
    {'a': {'b': Array(1., dtype=float32)}, 'c': Array(2, dtype=bfloat16)}
  """
  return jax.tree.map(lambda t, o: t.astype(o.dtype)
                      if hasattr(o, 'dtype') else t, tree, other_tree)

