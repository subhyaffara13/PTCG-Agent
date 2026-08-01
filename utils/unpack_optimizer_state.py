
def unpack_optimizer_state(opt_state):
  """Converts an OptimizerState to a marked pytree.

  Converts an OptimizerState to a marked pytree with the leaves of the outer
  pytree represented as JoinPoints to avoid losing information. This function is
  intended to be useful when serializing optimizer states.

  Args:
    opt_state: An OptimizerState
  Returns:
    A pytree with JoinPoint leaves that contain a second level of pytrees.
  """
  states_flat, tree_def, subtree_defs = opt_state
  subtrees = map(jax.tree.unflatten, subtree_defs, states_flat)
  sentinels = [JoinPoint(subtree) for subtree in subtrees]
  return jax.tree.unflatten(tree_def, sentinels)

