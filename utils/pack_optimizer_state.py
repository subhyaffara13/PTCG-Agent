
def pack_optimizer_state(marked_pytree):
  """Converts a marked pytree to an OptimizerState.

  The inverse of unpack_optimizer_state. Converts a marked pytree with the
  leaves of the outer pytree represented as JoinPoints back into an
  OptimizerState. This function is intended to be useful when deserializing
  optimizer states.

  Args:
    marked_pytree: A pytree containing JoinPoint leaves that hold more pytrees.
  Returns:
    An equivalent OptimizerState to the input argument.
  """
  sentinels, tree_def = jax.tree.flatten(marked_pytree)
  assert all(isinstance(s, JoinPoint) for s in sentinels)
  subtrees = [s.subtree for s in sentinels]
  states_flat, subtree_defs = unzip2(map(jax.tree.flatten, subtrees))
  return OptimizerState(states_flat, tree_def, subtree_defs)

