
def _tcgen05_mma_abstract_eval(acc, a, b, accumulate,
                               *barrier_scales_and_transforms_leaves,
                               acc_transforms_tree, a_transforms_tree,
                               b_transforms_tree,
                               barrier_transforms_tree,
                               a_scale_transforms_tree,
                               b_scale_transforms_tree,
                               a_sparse_metadata_transforms_tree,
                               collective_axis,
                               arrive,
                               scaled,
                               sparse):
  del accumulate, acc_transforms_tree, a_transforms_tree, b_transforms_tree, barrier_transforms_tree

  if acc.memory_space != gpu_core.TMEM:
    raise ValueError("Accumulator must be a TMEM Ref.")
  if a.memory_space not in (gpu_core.SMEM, gpu_core.TMEM):
    raise ValueError("LHS must be a TMEM/SMEM Ref.")
  if b.memory_space != gpu_core.SMEM:
    raise ValueError("RHS must be an SMEM Ref.")

  if collective_axis is not None:
    # TODO(justinfu): If under a core_map, the avals for acc/a
    # become normal MemRefs so we cannot check if they are collective.
    # Figure out a way to fix this.
    if isinstance(acc, gpu_core.AbstractTMEMRef) and not acc.collective:
      raise ValueError(
          "Accumulator Ref must be collective if collective_axis is set.")
    if isinstance(a, gpu_core.AbstractTMEMRef) and not a.collective:
      raise ValueError(
          "LHS Ref must be collective if collective_axis is set.")

  scales_and_transforms_leaves = barrier_scales_and_transforms_leaves
  if arrive:
    barrier, *scales_and_transforms_leaves = barrier_scales_and_transforms_leaves
    orders_tensor_core = getattr(
        barrier.inner_aval.dtype, "orders_tensor_core", False)
    if not orders_tensor_core:
      raise ValueError("MMA barrier must have orders_tensor_core set to True.")
  if scaled:
    a_scale, b_scale = scales_and_transforms_leaves[:2]
    if a_scale.memory_space != gpu_core.TMEM:
      raise ValueError("a_scale must be a TMEM Ref")
    if b_scale.memory_space != gpu_core.TMEM:
      raise ValueError("b_scale must be a TMEM Ref")

  return [], {gpu_core._memory_effect}

