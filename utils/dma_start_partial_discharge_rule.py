
def dma_start_partial_discharge_rule(
    should_discharge, in_avals, out_avals, *args, tree, device_id_type,
    priority, add
):
  # Note: we ignore the DMA priority in discharge rules.
  del priority
  if add:
    raise NotImplementedError(
        "DMA partial discharge add=True not yet implemented.")
  src_ref, dst_ref, dst_sem, src_sem, device_id = _dma_unflatten(tree, args)
  src_ref, src_transforms = _get_ref_and_transforms(src_ref)
  dst_ref, dst_transforms = _get_ref_and_transforms(dst_ref)
  dst_sem, dst_sem_transforms = _get_ref_and_transforms(dst_sem)
  src_sem, src_sem_transforms = _get_ref_and_transforms(src_sem)

  src_ref_aval, dst_ref_aval, dst_sem_aval, src_sem_aval, _ = _dma_unflatten(
      tree, in_avals
  )
  del out_avals

  _, dst_discharge, dst_sem_discharge, *maybe_src_sem_discharge = (
      _dma_unflatten(tree, should_discharge)
  )
  dst_discharge = _get_ref(dst_discharge)
  dst_sem_discharge = _get_ref(dst_sem_discharge)
  is_remote = device_id is not None
  src_sem_discharge = None

  if is_remote:
    src_sem_discharge = _get_ref(maybe_src_sem_discharge[0])

  if not is_remote:
    # Local async copies only use one semaphore.
    assert src_sem is None
    assert src_sem_transforms == ()

  num_src_sem_transforms = len(_dma_tree_leaves(src_sem_aval)) - 1
  num_dst_sem_transforms = len(_dma_tree_leaves(dst_sem_aval)) - 1
  num_src_transform_vals = len(_dma_tree_leaves(src_ref_aval)) - 1
  num_dst_transform_vals = len(_dma_tree_leaves(dst_ref_aval)) - 1

  updates = state_discharge.transform_array(src_ref[...], src_transforms)
  local_src = updates

  if is_remote:
    # Note that this code only works in SPMD mode. If not all devices execute
    # the DMA then the devices that do will hang.
    # TODO(justinfu): Verify that code only works in SPMD mode.
    axis_env = jax_core.get_axis_env()
    nonempty_axes = [name for name in axis_env.axis_sizes if name is not None]
    if isinstance(device_id, dict):
      if device_id_type is not primitives.DeviceIdType.MESH:
        raise ValueError(
            "`device_id_type` must be MESH if `device_id` is a dict,"
            f" got: {device_id_type = }."
        )
      device_id_list = []
      for axis in nonempty_axes:
        device_id_list.append(device_id.get(axis, jax.lax.axis_index(axis)))
      device_id = tuple(device_id_list)
    if device_id_type == primitives.DeviceIdType.LOGICAL:
      if len(nonempty_axes) > 1:
        raise NotImplementedError("Sharding with more than one named axis not "
                                  "implemented in dma_start_p for LOGICAL "
                                  "device_id_type.")
      shard_axis = nonempty_axes[0]
      my_axis = jax.lax.axis_index(shard_axis)
    elif device_id_type == primitives.DeviceIdType.MESH:
      device_id_len = 1
      if isinstance(device_id, jax.Array):
        device_id_len = device_id.size
      elif hasattr(device_id, '__len__'):
        device_id_len = len(device_id)
      if device_id_len != len(axis_env.axis_sizes):
        raise ValueError(
            f"device_id ({device_id_len}) and mesh ({len(axis_env.axis_sizes)}) "
            "must have same length.")
      if device_id_len > 1 or len(nonempty_axes) > 1:
        raise NotImplementedError("Meshes with more than 1 named dimension not "
                                  "implemented in dma_start_p")
      shard_axis = nonempty_axes[0]
      my_axis = jax.lax.axis_index(shard_axis)
    else:
      raise ValueError(f"Unknown device_id_type: {device_id_type}")
    # Compute the update that is being sent to the current device.
    who_copy_to_me = jax.lax.all_gather(device_id, shard_axis) == my_axis
    # TODO(justinfu): Add a checkify for verifying there is at most one source.
    # TODO(justinfu): Handle the case where no other device is copying to
    # this device.
    index = jnp.argmax(who_copy_to_me, axis=0)
    global_updates = jax.lax.all_gather(updates, shard_axis)
    updates = jax.lax.dynamic_index_in_dim(
        global_updates, index, axis=0, keepdims=False)

    # Handle asymmetrical indexing when devices do not share the same
    # dst_transform.
    global_dst_transforms = tree_util.tree_map(
        lambda x: jax.lax.all_gather(x, shard_axis), dst_transforms
    )
    dst_transforms = tree_util.tree_map(
        lambda x: jax.lax.dynamic_index_in_dim(
            x, index, axis=0, keepdims=False
        ),
        global_dst_transforms,
    )

  def do_discharge_dst(dst_ref=dst_ref):
    _, ret = state_discharge.transform_swap_array(
        dst_ref, dst_transforms, updates
    )
    return ret

  # Update semaphore values.
  # TODO(justinfu): Potentially handle asymmetric copy sizes.
  def do_discharge_dst_sem(dst_sem=dst_sem):
    recv_size = jnp.minimum(updates.size, pl_core.SEMAPHORE_MAX_VALUE)
    recv_size = jnp.array(recv_size, dtype=pl_core.SEMAPHORE_INTERPRET_DTYPE)
    dst_sem_value = primitives._transform_semaphore(
        dst_sem, dst_sem_transforms, _get_ref(dst_sem_aval)
    )
    _, ret = state_discharge.transform_swap_array(
        dst_sem, dst_sem_transforms, dst_sem_value[...] + recv_size
    )
    return ret

  def do_discharge_src_sem(src_sem=src_sem):
    send_size = jnp.minimum(local_src.size, pl_core.SEMAPHORE_MAX_VALUE)
    send_size = jnp.array(send_size, dtype=pl_core.SEMAPHORE_INTERPRET_DTYPE)
    src_sem_value = primitives._transform_semaphore(
        src_sem, src_sem_transforms, _get_ref(src_sem_aval)
    )
    _, ret = state_discharge.transform_swap_array(
        src_sem, src_sem_transforms, src_sem_value[...] + send_size
    )
    return ret

  new_vals = (None,)  # src_val
  new_vals += (None,) * num_src_transform_vals
  new_vals += (do_discharge_dst() if dst_discharge else None,)  # dst_val
  new_vals += (None,) * num_dst_transform_vals
  new_vals += (do_discharge_dst_sem() if dst_sem_discharge else None,)  # dst_sem
  new_vals += (None,) * num_dst_sem_transforms
  if is_remote:
    new_vals += (do_discharge_src_sem() if src_sem_discharge else None,) # src_sem
    new_vals += (None,) * num_src_sem_transforms
    new_vals += (None,)  # device_id
  assert (len(new_vals) ==
          len(in_avals)), f"{len(new_vals), new_vals} != {len(in_avals)}"

  # If we didn't discharge everything we could we should keep writes
  # to the references that are left over.
  if not dst_discharge:
    sp.ref_set(dst_ref, None, do_discharge_dst(dst_ref=dst_ref[...]))
  if not dst_sem_discharge:
    sp.ref_set(dst_sem, None, do_discharge_dst_sem(dst_sem=dst_sem[...]))
  if is_remote and not src_sem_discharge:
    sp.ref_set(src_sem, None, do_discharge_src_sem(src_sem=src_sem[...]))

  return new_vals, []

