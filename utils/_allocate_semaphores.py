
def _allocate_semaphores(
    token: Array, device_id: Array, local_core_id: Array | None, shape: Array
):
  """Allocates semaphores on the device with id `device_id` and core with id `local_core_id`.

  The number of semaphores allocated is given by the product of the entries in
  `shape`.

  Since for each semaphore id there is really only one global `Semaphore`
  object, 'allocation' of semaphores per device and core here means that the
  internal counter of semaphore ids that is held by `SharedMemory` is
  incremented for each the device and core (or for all cores on the dive if
  argument `local_core_id` is None, see below).

  Args:
    device_id: Singleton array holding the id for the device where the
      semaphores will be allocated.
    local_core_id: None or singleton array holding the id for the core where the
      semaphores will be allocated. If None, semaphores will be allocated on all
      cores on the device.
    shape: Shape of the semaphore array to allocate.

  Returns:
    Array of semaphore ids.
  """
  device_id: int = int(device_id)  # pyrefly: ignore[redefinition]
  shape: tuple[int, ...] = tuple(map(int, shape))  # pyrefly: ignore[redefinition]
  num_semaphores = math.prod(shape)

  shared_memory = _get_shared_memory()

  if local_core_id is None:
    local_core_id_int = 0
    global_core_ids = shared_memory.get_global_core_ids(device_id)
  else:
    local_core_id_int = int(local_core_id)
    global_core_ids = (
        shared_memory.get_global_core_id(device_id, local_core_id_int),
    )
  del local_core_id

  global_core_id_to_semaphore_id = {}
  for gci in global_core_ids:
    semaphore_id = shared_memory.allocate_semaphores(gci, num_semaphores)
    global_core_id_to_semaphore_id[gci] = semaphore_id

  global_core_id = shared_memory.get_global_core_id(
      device_id, local_core_id_int
  )
  # The semaphore ids should always be kept in sync across all cores.
  assert all(
      semaphore_id == global_core_id_to_semaphore_id[global_core_id]
      for semaphore_id in global_core_id_to_semaphore_id.values()
  )

  # NOTE: For now, we use a relatively uncommon datatype (int16) for
  # semaphore (and buffer) IDs, so these values are more easily identifiable
  # in kernels.
  #
  # TODO(jburnim): Raise an error if any IDs are too big for int16.
  semaphore_id = global_core_id_to_semaphore_id[global_core_id]
  return token, np.arange(
      semaphore_id, semaphore_id + num_semaphores, dtype=np.int16
  ).reshape(shape)

