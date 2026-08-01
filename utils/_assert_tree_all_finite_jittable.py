
def _assert_tree_all_finite_jittable(tree_like: ArrayTree) -> Array:
  """A jittable version of `_assert_tree_all_finite_static`."""
  labeled_tree = jax.tree.map(
      lambda x: jax.lax.select(jnp.isfinite(x).all(), .0, jnp.nan), tree_like
  )
  predicate = jnp.all(
      jnp.isfinite(jnp.asarray(jax.tree_util.tree_leaves(labeled_tree)))
  )
  checkify.check(
      pred=predicate,
      msg="Tree contains non-finite value: {tree}.",
      tree=labeled_tree,
  )
  return predicate

