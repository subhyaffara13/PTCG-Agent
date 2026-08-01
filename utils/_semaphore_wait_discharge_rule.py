
def _semaphore_wait_discharge_rule(in_avals,
                                     out_avals,
                                     *flat_args,
                                     args_tree):
  del out_avals
  [ref, transforms, value, decrement] = args_tree.unflatten(flat_args)
  sem_value = _transform_semaphore(ref, transforms, in_avals[0])
  value = value.astype(pallas_core.SEMAPHORE_INTERPRET_DTYPE)
  if decrement:
    _, new_sem_value = state_discharge.transform_swap_array(
        ref, transforms, sem_value - value
    )
  else:
    new_sem_value = sem_value
  return (new_sem_value,) + (None,) * (len(in_avals) - 1), ()

