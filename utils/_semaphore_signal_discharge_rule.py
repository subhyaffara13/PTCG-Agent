
def _semaphore_signal_discharge_rule(in_avals,
                                     out_avals,
                                     *flat_args,
                                     args_tree,
                                     device_id_type):
  del out_avals, device_id_type
  [ref, transforms, inc, device_id, core_index] = args_tree.unflatten(flat_args)
  if device_id is not None:
    raise NotImplementedError("Remote signal not implemented.")
  if core_index is not None:
    raise NotImplementedError("Multiple core support not implemented.")
  sem_value = _transform_semaphore(ref, transforms, in_avals[0])
  inc = inc.astype(pallas_core.SEMAPHORE_INTERPRET_DTYPE)
  _, new_sem_value = state_discharge.transform_swap_array(
      ref, transforms, sem_value + inc
  )
  return (new_sem_value,) + (None,) * (len(in_avals) - 1), ()

