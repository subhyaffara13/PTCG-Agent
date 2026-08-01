
def get_pathways_array_handler(
    use_single_replica_array_handler: bool = False,
    checkpointing_impl: CheckpointingImpl | None = None,
    **kwargs,
) -> type_handlers.ArrayHandler:
  """Returns the Pathways ArrayHandler with the given options."""

  # If not set, use whichever dispatcher implementation is available.
  checkpointing_impl = checkpointing_impl or CheckpointingImpl.from_options(
      use_colocated_python=True,
      use_persistence_array_handler=True,
  )
  match checkpointing_impl:
    case CheckpointingImpl.COLOCATED_PYTHON:
      logging.info('Using ColocatedPythonDispatcher')
      dispatcher = dispatchers.ColocatedPythonDispatcher()
    case CheckpointingImpl.PERSISTENCE:
      logging.info('Using persistence array handler for jax.Array.')
      return _get_pathways_persistence_array_handler(**kwargs)
    case CheckpointingImpl.NO_DISPATCHER:
      logging.info('Not using dispatcher')
      dispatcher = None
    case _:
      raise ValueError(f'Unsupported CheckpointingImpl: {checkpointing_impl}')

  return _get_array_hander_with_dispatcher(
      dispatcher,
      use_single_replica_array_handler,
      **kwargs,
  )

