
def semaphore_signal(
    sem_or_view,
    inc: int | jax_typing.Array = 1,
    *,
    device_id: DeviceId = None,
    device_id_type: DeviceIdType = DeviceIdType.MESH,
    core_index: int | jax_typing.Array | None = None,
):
  """Increments the value of a semaphore.

  This operation can also be performed remotely if ``device_id`` is specified,
  in which ``sem_or_view`` refers to a Ref located on another device.
  Note that it is assumed that ``sem_or_view`` is already allocated
  (e.g. through the proper use of barriers), or else this operation could
  result in undefined behavior.

  Args:
    sem_or_view: A Ref (or view) representing a semaphore.
    inc: The value to increment by.
    device_id (optional): Specifies which device to signal.
      If not specified, ``sem_or_view`` is assumed to be local.
    device_id_type (optional): The format in which
      ``device_id`` should be specified.
    core_index (optional): If on a multi-core device,
      specifies which core to signal.
  """
  ref, transforms = _get_ref_and_transforms(sem_or_view)
  inc = jnp.asarray(inc, dtype=jnp.int32)
  args = [ref, transforms, inc, device_id, core_index]
  flat_args, args_tree = tree_util.tree_flatten(args)
  semaphore_signal_p.bind(
      *flat_args,
      args_tree=args_tree,
      device_id_type=device_id_type,
  )


def semaphore_signal(
    semaphore,
    inc: int | jax.Array = 1,
    *,
    device_id: pallas_primitives.DeviceId | None = None,
    memory_scope: Literal["sys", "gpu"] = "sys",
):
  """Signals a semaphore, optionally on a remote device.

  This is the MGPU specific variant of :func:`pallas.semaphore_signal`,
  which additionally exposes the ``memory_scope`` of the underlying atomic.

  Args:
    semaphore: The semaphore reference to signal.
    inc: The increment value for the semaphore.
    device_id: Optional logical device id at which to signal the semaphore.
    memory_scope: The memory scope of the underlying atomic. Must be ``"sys"``
      or ``"gpu"``. Defaults to ``"sys"``.
  """
  ref, transforms = pallas_primitives._get_ref_and_transforms(semaphore)
  value = jnp.asarray(inc, dtype=jnp.int32)
  core_index = None
  args = [ref, transforms, value, device_id, core_index]
  flat_args, args_tree = tree_util.tree_flatten(args)
  semaphore_signal_p.bind(
      *flat_args,
      args_tree=args_tree,
      device_id_type=pallas_primitives.DeviceIdType.MESH,
      memory_scope=memory_scope,
  )


def semaphore_signal(
    token,
    device_id,
    local_core_id,
    sem_id,
    inc,
    target_device_id,
    target_local_core_id,
    source_info=None,
):
  shared_memory = _get_shared_memory()

  device_id = int(device_id)
  local_core_id = int(local_core_id)
  sem_id = int(sem_id)
  inc = int(inc)
  src_global_core_id = shared_memory.get_global_core_id(
      device_id, local_core_id
  )
  if target_device_id is None:
    target_device_id = device_id
  else:
    target_device_id = int(target_device_id)
  if target_local_core_id is None:
    target_local_core_id = 0

  (sem,), clock = shared_memory.get_semaphores_and_increment_clock(
      [sem_id], src_global_core_id
  )
  assert sem is not None
  sem.signal(
      inc,
      shared_memory.get_global_core_id(target_device_id, target_local_core_id),
      clock,
      logging_info=interpret_utils.TPULoggingInfo(
          device_id=device_id,
          local_core_id=local_core_id,
          source_info=source_info,
      ),
  )
  return token

