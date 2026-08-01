
def force_tpu_interpret_mode(params: InterpretParams = InterpretParams()):
  """Context manager that forces TPU interpret mode under its dynamic context.

  TPU interpret mode is a way run Pallas TPU kernels on CPU, while simulating
  a TPU's shared memory (HBM, VMEM, etc.), communication (remote and local
  DMAs), and synchronization operations (semaphores, barriers, etc.).  This mode
  is intended for debugging and testing.  See :class:`InterpretParams` for
  additional information.

  Args:
    params: an instance of :class:`InterpretParams`.  Any call to
      :func:`jax.experimental.pallas.pallas_call` or
      :func:`jax.experimental.pallas.core_map` that is traced under this context
      manager will be run with ``interpret=params``.  When ``params`` is not
      ``None``, this will cause those calls to run with TPU interpret mode.
  """
  prev = config.pallas_tpu_interpret_mode_context_manager.swap_local(params)
  try:
    yield
  finally:
    config.pallas_tpu_interpret_mode_context_manager.set_local(prev)

