
def dma_wait_partial_discharge_rule(
    should_discharge,
    in_avals,
    out_avals,
    *args,
    tree,
    device_id_type,
    insert_dummy_device: bool,
):
  # TODO(b/370563115): perform ref update in dma_wait discharge rule instead of dma_start
  del out_avals, device_id_type, insert_dummy_device
  _, dst_ref, dst_sem, _, _ = _dma_unflatten(tree, args)
  dst_ref, dst_ref_transforms = _get_ref_and_transforms(dst_ref)
  dst_sem, dst_sem_transforms = _get_ref_and_transforms(dst_sem)
  src_ref_aval, dst_ref_aval, dst_sem_aval, src_sem_aval, device_id_aval = (
      _dma_unflatten(tree, in_avals)
  )

  # The only one we can discharge is the dst semaphore. The provided
  # buffers are only specified for their types and not their value so
  # it's completely irrelevant for us here if they are discharged.
  should_discharge_unflattened = _dma_unflatten(tree, should_discharge)
  if not _get_ref(should_discharge_unflattened[2]):
    return (None,) * len(in_avals), []

  num_sem_transforms = len(_dma_tree_leaves(dst_sem_aval)) - 1
  num_src_transform_vals = len(_dma_tree_leaves(src_ref_aval)) - 1
  num_transforms = len(_dma_tree_leaves(dst_ref_aval)) - 1
  updates = state_discharge.transform_array(dst_ref[...], dst_ref_transforms)
  copy_size = jnp.minimum(updates.size, pl_core.SEMAPHORE_MAX_VALUE)
  copy_size = jnp.array(copy_size, dtype=pl_core.SEMAPHORE_INTERPRET_DTYPE)
  sem_value = primitives._transform_semaphore(
      dst_sem, dst_sem_transforms, _get_ref(dst_sem_aval)
  )
  _, new_sem = state_discharge.transform_swap_array(
      dst_sem, dst_sem_transforms, sem_value - copy_size
  )
  new_vals = (None,)  # src_ref
  new_vals += (None,) * num_src_transform_vals
  new_vals += (None,)  # ref
  new_vals += (None,) * num_transforms  # ref_transforms
  new_vals += (new_sem,)  # sem
  new_vals += (None,) * num_sem_transforms
  new_vals += (None,) * len(tree_util.tree_leaves(src_sem_aval))  # src_sem
  new_vals += (None,) * len(tree_util.tree_leaves(device_id_aval)) # device_id
  return new_vals, []

