
def _tree_sum_squares(tree):
  leaves = jax.tree.leaves(tree)
  return sum(jnp.sum(jnp.square(x.astype(jnp.float32))) for x in leaves)

