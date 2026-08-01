
def reset_tpu_interpret_mode_state():
  """Resets all global, shared state used by TPU interpret mode.

  TPU interpret mode uses global, shared state for simulating memory buffers
  and semaphores, for race detection, etc., when interpreting a kernel.
  Normally, this shared state is cleaned up after a kernel is interpreted.

  But if an exception is thrown while interpreting a kernel, the shared state
  is not cleaned up, allowing the simulated TPU state to be examined for
  debugging purposes.  In this case, the shared state must be reset before
  any further kernels are interpreted.
  """
  global _shared_memory, races, dma_id_counter
  with _shared_memory_init_lock:
    _shared_memory = None
    races = None
    dma_id_counter = None

