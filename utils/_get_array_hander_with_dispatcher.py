import logging

def _get_array_hander_with_dispatcher(
    dispatcher: dispatchers.Dispatcher | None,
    use_single_replica_array_handler: bool,
    **kwargs,
) -> type_handlers.ArrayHandler:
  """Returns the Pathways ArrayHandler."""
  # Inject default array_metadata_store if not provided
  if 'array_metadata_store' not in kwargs:
    logging.warn('Array Metadata Store not specified, setting to default Store')
    kwargs['array_metadata_store'] = array_metadata_store_lib.Store()
  if use_single_replica_array_handler:
    logging.info('Using SingleReplicaArrayHandler')
    return jax_array_handlers.SingleReplicaArrayHandler(
        dispatcher=dispatcher, **kwargs
    )
  else:
    return jax_array_handlers.ArrayHandler(dispatcher=dispatcher, **kwargs)

