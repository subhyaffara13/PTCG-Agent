
def _semaphore_wait_abstract_eval(*avals, args_tree):
  sem_aval, sem_transforms_avals, value_aval, _ = tree_util.tree_unflatten(
      args_tree, avals
  )
  check_sem_avals(sem_aval, sem_transforms_avals, "wait")
  if value_aval.dtype != jnp.dtype("int32"):
    raise ValueError("Must wait an int32 value.")
  return [], {sem_effect}


def _semaphore_wait_abstract_eval(*avals, args_tree, memory_scope):
  del memory_scope  # Unused.
  return pallas_primitives.semaphore_wait_p.abstract_eval(
      *avals, args_tree=args_tree
  )

