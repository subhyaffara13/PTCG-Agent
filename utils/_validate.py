
def _validate(params: str) -> bool:
    """Validate the presence of the tag name after the marker."""
    tag = params.strip().split(" ", 1)[-1] or ""
    return bool(tag)


def _validate(token, device_id):
  device_id = int(device_id)

  shared_memory = _get_shared_memory()
  semaphores = shared_memory.get_sempahores_with_nonzero_count(device_id)
  if semaphores:
    sem, global_core_id = semaphores[0]
    # TODO(jburnim): Make this raise an error, but in a way that doesn't
    # cause other devices to hang later in `_clean_up_shared_memory`.
    print(
        f'Semaphore {sem.id} has non-zero count for {device_id} (global core'
        f' {global_core_id}) at kernel exit:'
        f' {sem.count_by_core[global_core_id]}'
    )
  return token

