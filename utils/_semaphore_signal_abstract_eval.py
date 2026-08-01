
def _semaphore_signal_abstract_eval(
    *avals,
    args_tree,
    device_id_type: DeviceIdType,
):
  (
      sem_aval,
      sem_transforms_avals,
      value_aval,
      device_id_aval,
      core_index_aval,
  ) = tree_util.tree_unflatten(args_tree, avals)
  check_sem_avals(sem_aval, sem_transforms_avals, "signal")
  if value_aval.dtype != jnp.dtype("int32"):
    raise ValueError(f"Must signal an int32 value, but got {value_aval.dtype}")
  effs: set[effects.Effect] = {sem_effect}
  if device_id_aval is not None:
    device_id_flat_avals = tree_util.tree_leaves(device_id_aval)
    for aval in device_id_flat_avals:
      if aval.dtype != jnp.dtype("int32"):
        raise ValueError(
            f"`device_id`s must be an int32 value, but got {aval.dtype}"
        )
    if device_id_type is DeviceIdType.MESH and isinstance(device_id_aval, dict):
      for k in device_id_aval:
        if not isinstance(k, tuple):
          k = (k,)
        for k_ in k:
          effs.add(jax_core.NamedAxisEffect(k_))
    else:
      effs.add(pallas_core.comms_effect)
  return [], effs


def _semaphore_signal_abstract_eval(
    *avals, args_tree, device_id_type, memory_scope
):
  del memory_scope  # Unused.
  return pallas_primitives.semaphore_signal_p.abstract_eval(
      *avals, args_tree=args_tree, device_id_type=device_id_type
  )

