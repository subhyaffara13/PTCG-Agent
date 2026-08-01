
def tree_map_rngs(fn, tree):
  """Needed for mapping JAX random.* functions over PRNGKey leaves."""
  return jax.tree_util.tree_map(
    fn,
    tree,
    is_leaf=lambda x: hasattr(x, 'dtype')
    and jax.dtypes.issubdtype(x.dtype, jax.dtypes.prng_key),
  )

