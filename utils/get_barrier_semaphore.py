
def get_barrier_semaphore():
  """Returns a barrier semaphore.

  This function returns a barrier semaphore based on the collective_id of the
  current pallas kernel.

  It's very important that the semaphore is wait-ed back down to 0, or else the
  semaphores will become corrupted.

  It's also very important that the collective_id is different for each pallas
  kernel with communication. E.g. if you have two pallas kernels, one that syncs
  across the X axis of the device mesh and the second that syncs across the Y
  axis, they must have different collective_ids.
  However it is legal for two kernels that perform the same synchronization
  pattern (e.g. only communicating with neighbours on the same mesh axis)
  to share a collective_id. However, if in doubt, prefer not sharing
  collective_ids, as doing so incorrectly can lead to silent data corruption or
  crashes.
  Note that reusing the same collective_id doesn't guarantee that the same
  semaphore is provided by XLA.
  """
  return get_barrier_semaphore_p.bind()


def get_barrier_semaphore(token, device_id, collective_id):
  del device_id
  collective_id = int(collective_id)
  shared_memory = _get_shared_memory()
  shared_memory.guarantee_semaphore_with_fixed_id(collective_id)
  return token, np.int16(collective_id)

