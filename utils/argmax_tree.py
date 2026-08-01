
def argmax_tree(x):
  return jax.tree.map(one_hot_argmax, x)

