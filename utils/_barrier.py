
def _barrier(worker_names):
    r"""
    Synchronizes local and remote RPC processes.

    This will block until all local and remote RPC processes specified under worker_names
    reach this method to wait for all outstanding work to complete.

    Args:
        worker_names (List[str]): The set of workers to synchronize.

    """
    try:
        _all_gather(None, set(worker_names))
    except RuntimeError:
        logger.exception("Failed to complete barrier")


def _barrier(token, device_id):
  del device_id
  shared_memory = _get_shared_memory()
  if shared_memory.num_devices > 1:
    shared_memory.barrier.wait()
  return token

