
def reset_gpu_interpret_mode_state():
  """Resets all global, shared state used by GPU interpret mode.

  GPU interpret mode uses global, shared state for simulating memory buffers,
  for race detection, etc., when interpreting a kernel. Normally, this shared
  state is cleaned up after a kernel is interpreted.

  But if an exception is thrown while interpreting a kernel, the shared state
  is not cleaned up, allowing the simulated GPU state to be examined for
  debugging purposes. In this case, the shared state must be reset before
  any further kernels are interpreted.
  """
  global _shared_memory, _races
  with _shared_memory_init_lock:
    _shared_memory = None
    _races = None


def reset_gpu_interpret_mode_state():
  gpu_callbacks.reset_gpu_interpret_mode_state()

