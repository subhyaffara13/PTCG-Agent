
def _sync_op_id_generator(test_file_yaml: str) -> None:
  """Synchronizes the OperationIdGenerator across processes."""
  try:
    client = multihost.get_jax_distributed_client()
    if client is not None:
      normalized_name = test_file_yaml.replace('/', '_').replace(':', '_')
      sync_key = f'sync_op_id_file_{normalized_name}'
      operation_id_generator = synchronization.OperationIdGenerator
      if jax.process_index() == 0:
        client.key_value_set(
            sync_key,
            operation_id_generator.get_current_operation_id(),
            allow_overwrite=True,
        )
      target = int(client.blocking_key_value_get(sync_key, 10000))
      while int(operation_id_generator.get_current_operation_id()) < target:
        operation_id_generator.next_operation_id()
  except Exception as sync_e:  # pylint: disable=broad-exception-caught
    logging.warning(
        'Could not synchronize OperationIdGenerator for file: %s', sync_e
    )

