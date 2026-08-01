
def force_gpu_interpret_mode(params: InterpretGPUParams = InterpretGPUParams()):
  """Context manager that forces GPU interpret mode under its dynamic context.

  See :class:`InterpretGPUParams` for additional information.

  Args:
    params: an instance of :class:`InterpretGPUParams`.  Any call to
       :func:`jax.experimental.pallas.mosaic_gpu.kernel`,
      :func:`jax.experimental.pallas.core_map`, or
      :func:`jax.experimental.pallas.pallas_call` that is traced under this
      context manager will be run with ``interpret=params``.  When ``params``
      is not``None``, this will cause those calls to run with GPU
      interpret mode.
  """
  # TODO(jburnim): Rename to config.pallas_interpret_mode_context_manager.
  prev = config.pallas_tpu_interpret_mode_context_manager.swap_local(params)
  try:
    yield
  finally:
    config.pallas_tpu_interpret_mode_context_manager.set_local(prev)

