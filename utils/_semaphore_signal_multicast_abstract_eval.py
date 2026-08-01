
def _semaphore_signal_multicast_abstract_eval(
    *avals, args_tree, collective_axes
):
  del collective_axes  # Unused.
  sem_aval, transform_avals, _ = tree_util.tree_unflatten(args_tree, avals)
  pallas_primitives.check_sem_avals(
      sem_aval, transform_avals, "semaphore_signal_multicast"
  )
  return (), {pallas_core.comms_effect}

