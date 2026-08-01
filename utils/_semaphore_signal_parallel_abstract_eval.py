
def _semaphore_signal_parallel_abstract_eval(*avals, args_tree):
  (
      sem_avals,
      sem_transforms_avals,
      value_avals,
      device_id_avals,
  ) = tree_util.tree_unflatten(args_tree, avals)
  for sem_aval, sem_transform_avals in zip(sem_avals, sem_transforms_avals, strict=True):
    pallas_primitives.check_sem_avals(sem_aval, sem_transform_avals, "signal")
  if any(va.dtype != jnp.dtype("int32") for va in value_avals):
    raise ValueError(
        "Must signal int32 values, but got"
        f" {[aval.dtype for aval in value_avals]}"
    )
  effs = set()
  for device_id in device_id_avals:
    if device_id is not None:
      device_id_flat_avals = tree_util.tree_leaves(device_id)
      for aval in device_id_flat_avals:
        if aval.dtype != jnp.dtype("int32"):
          raise ValueError(
             f"`device_id`s must be int32 values, but got {aval.dtype}"
          )
      effs.add(pallas_core.comms_effect)
  return [], effs

