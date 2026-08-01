
def _tcgen05_commit_arrive_abstract_eval(barrier,
                               *barrier_transforms_leaves,
                               barrier_transforms_tree,
                               collective_axis):
  del barrier_transforms_leaves, barrier_transforms_tree, collective_axis
  orders_tensor_core = getattr(
      barrier.inner_aval.dtype, "orders_tensor_core", False)
  if not orders_tensor_core:
    raise ValueError("MMA barrier must have orders_tensor_core set to True.")
  return [], {gpu_core._memory_effect}

