
def _clean_up_shared_memory(token):
  shared_memory = _get_shared_memory()
  shared_memory.clean_up_barrier.wait()
  return token


def _clean_up_shared_memory(token, device_id):
  del device_id
  shared_memory = _get_shared_memory()
  # NOTE: We rely on the fact that `clean_up_barrier.wait()` will not raise.
  # Otherwise, we could end up waiting on the barrier once here, and then again
  # in the fail_on_exception wrapper -- so the barrier could complete without
  # all devices having reached it.
  shared_memory.clean_up_barrier.wait()
  return token

