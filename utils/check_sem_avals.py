
def check_sem_avals(
    sem_aval, sem_transforms_avals, name, allowed_semaphore_types=None
):
  if allowed_semaphore_types is None:
    allowed_semaphore_types = {
        pallas_core.semaphore,
        pallas_core.barrier_semaphore,
        # For interpret mode.
        pallas_core.SEMAPHORE_INTERPRET_DTYPE,
    }
  if not isinstance(sem_aval, state.AbstractRef):
    raise ValueError(f"Cannot {name} on a non-semaphore Ref: {sem_aval}")
  sem_shape = sem_aval.shape
  if sem_transforms_avals:
    sem_shape = sem_transforms_avals[-1].get_indexer_shape()
  if sem_shape:
    raise ValueError(f"Cannot {name} on a non-()-shaped semaphore: {sem_shape}")
  sem_dtype = sem_aval.dtype
  if not any(
      jnp.issubdtype(sem_dtype, sem_type)
      for sem_type in allowed_semaphore_types
  ):
    raise ValueError(
        f"Must {name} semaphores of the following types:"
        f" {allowed_semaphore_types}. Got {sem_dtype}."
    )

