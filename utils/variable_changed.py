
def variable_changed(post: variablelib.Variable, pre: variablelib.Variable) -> bool:
  post_leaves, post_td = jax.tree.flatten(post)
  pre_leaves, pre_td = jax.tree.flatten(pre)
  return post_td != pre_td or any(  # type: ignore[operator]
    a is not b for a, b in zip(post_leaves, pre_leaves)
  )

