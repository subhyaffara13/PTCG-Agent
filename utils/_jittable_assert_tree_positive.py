
def _jittable_assert_tree_positive(tree):
  # Jittable version of `_assert_tree_positive`.
  pred = jnp.all(
      jnp.array([(x > 0).all() for x in jax.tree_util.tree_leaves(tree)]))
  asserts_chexify.checkify.check(pred, 'Tree contains non-positive elems!')
  return pred

