
def _semaphore_read_discharge_rule(in_avals,
                                   out_avals,
                                   *flat_args,
                                   args_tree):
  del out_avals
  [ref, transforms] = args_tree.unflatten(flat_args)
  sem_value = _transform_semaphore(ref, transforms, in_avals[0])
  sem_value = sem_value.astype(jnp.int32)
  return (None,) * len(in_avals), sem_value

