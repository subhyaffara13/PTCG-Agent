
def semaphore_wait(
    sem_or_view, value: int | jax_typing.Array = 1, *, decrement: bool = True
):
  """Blocks execution of the current thread until a semaphore reaches a value.

  Args:
    sem_or_view: A Ref (or view) representing a semaphore.
    value: The target value that the semaphore should reach before unblocking.
    decrement: Whether to decrement the value of the semaphore after
      a successful wait.
  """
  ref, transforms = _get_ref_and_transforms(sem_or_view)
  value = jnp.asarray(value, dtype=jnp.int32)
  args = [ref, transforms, value, decrement]
  flat_args, args_tree = tree_util.tree_flatten(args)
  semaphore_wait_p.bind(*flat_args, args_tree=args_tree)


def semaphore_wait(
    semaphore,
    value: int | jax.Array = 1,
    *,
    decrement: bool = True,
    memory_scope: Literal["sys", "gpu"] = "sys",
):
  """Waits on a semaphore until it reaches at least ``value``.

  This is the MGPU specific variant of :func:`pallas.semaphore_wait`,
  which additionally exposes the ``memory_scope`` of the underlying atomic.

  Args:
    semaphore: The semaphore reference to wait on.
    value: The target value that the semaphore should reach before unblocking.
    decrement: Whether to decrement the semaphore by ``value`` once the wait
      succeeds.
    memory_scope: The memory scope of the underlying atomic. Must be ``"sys"``
      or ``"gpu"``. Defaults to ``"sys"``.
  """
  ref, transforms = pallas_primitives._get_ref_and_transforms(semaphore)
  value = jnp.asarray(value, dtype=jnp.int32)
  args = [ref, transforms, value, decrement]
  flat_args, args_tree = tree_util.tree_flatten(args)
  semaphore_wait_p.bind(
      *flat_args,
      args_tree=args_tree,
      memory_scope=memory_scope,
  )


def semaphore_wait(
    token, device_id, local_core_id, sem_id, value, source_info=None
):
  shared_memory = _get_shared_memory()

  device_id = int(device_id)
  local_core_id = int(local_core_id)
  sem_id = int(sem_id)
  value = int(value)
  global_core_id = shared_memory.get_global_core_id(device_id, local_core_id)

  (sem,), _ = shared_memory.get_semaphores_and_increment_clock(
      [sem_id], global_core_id
  )
  assert sem is not None
  sem.wait(
      value,
      global_core_id,
      logging_info=interpret_utils.TPULoggingInfo(
          device_id=device_id,
          local_core_id=local_core_id,
          source_info=source_info,
      ),
  )
  return token

