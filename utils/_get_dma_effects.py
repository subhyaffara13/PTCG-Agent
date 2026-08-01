
def _get_dma_effects(
    src_ref_aval,
    dst_ref_aval,
    dst_sem_aval,
    src_sem_aval,
    device_id_aval,
    device_id_type,
):
  n_src_transforms = len(_dma_tree_leaves(src_ref_aval))
  n_dst_transforms = len(_dma_tree_leaves(dst_ref_aval))
  n_dst_sem_transforms = len(_dma_tree_leaves(dst_sem_aval))
  dst_sem_index = n_src_transforms + n_dst_transforms
  effs: set[jax_core.Effect] = {
      state.ReadEffect(0),  # Read from src ref
      state.WriteEffect(n_src_transforms),  # Write to dst ref
      state.WriteEffect(dst_sem_index),  # Write to dst sem
  }
  if src_sem_aval is not None:
    src_sem_index = n_src_transforms + n_dst_transforms + n_dst_sem_transforms
    effs.add(state.WriteEffect(src_sem_index))
  if device_id_aval is not None:
    if device_id_type is primitives.DeviceIdType.MESH and isinstance(
        device_id_aval, dict
    ):
      for k in device_id_aval:
        if not isinstance(k, tuple):
          k = (k,)
        for k_ in k:
          effs.add(jax_core.NamedAxisEffect(k_))
  return effs

